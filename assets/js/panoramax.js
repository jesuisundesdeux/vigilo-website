/*
 * Panoramax (https://panoramax.fr): street-level pictures, searched through the
 * federated catalog (all the Panoramax instances) and shown in its viewer.
 */
const PANORAMAX_URL = 'https://explore.panoramax.fr';

let searchEndpoint;

function getSearchEndpoint() {
	if (!searchEndpoint) {
		// STAC landing page: its "search" link gives the search endpoint
		searchEndpoint = fetch(PANORAMAX_URL + '/api')
			.then((r) => r.json())
			.then((landing) => {
				const link = (landing.links || []).find((l) => l.rel === 'search');
				return link ? new URL(link.href, PANORAMAX_URL + '/api/').href : PANORAMAX_URL + '/api/search';
			})
			.catch(() => PANORAMAX_URL + '/api/search');
	}
	return searchEndpoint;
}

/**
 * Nearest picture around (lat, lon), within radius (degrees), or null
 */
export async function findPicture(lat, lon, radius) {
	try {
		const endpoint = await getSearchEndpoint();
		const bbox = [lon - radius, lat - radius, lon + radius, lat + radius].map((d) => d.toFixed(7)).join(',');
		const r = await fetch(endpoint + '?bbox=' + bbox + '&limit=50');
		if (!r.ok) {
			return null;
		}
		const features = ((await r.json()).features || []).filter((f) => f.id && f.geometry && f.geometry.coordinates);
		if (!features.length) {
			return null;
		}
		const dist = (f) => (f.geometry.coordinates[0] - lon) ** 2 + (f.geometry.coordinates[1] - lat) ** 2;
		const nearest = features.reduce((a, b) => (dist(b) < dist(a) ? b : a));
		const [plon, plat] = nearest.geometry.coordinates;
		return {
			id: nearest.id,
			lat: plat,
			lon: plon,
			// same link as the "open on Panoramax" one of the Panoramax viewer
			url: PANORAMAX_URL + '/?pic=' + encodeURIComponent(nearest.id),
			// viewer focused on the picture, with the map around (embeddable, as offered by its share menu)
			embedUrl: PANORAMAX_URL + '/#focus=pic&pic=' + encodeURIComponent(nearest.id) + '&map=18/' + plat + '/' + plon
		};
	} catch (e) {
		return null;
	}
}

let dialog;

function getDialog() {
	if (!dialog) {
		dialog = document.createElement('dialog');
		dialog.className = 'panoramax-dialog';
		dialog.innerHTML = '<div class="panoramax-dialog-body"><iframe title="Visionneuse Panoramax" allow="fullscreen; clipboard-write" allowfullscreen></iframe></div>'
			+ '<div class="panoramax-dialog-footer">'
			+ '<a class="btn btn-ghost panoramax-open" target="_blank" rel="noopener">Ouvrir dans Panoramax ↗</a>'
			+ '<button type="button" class="btn btn-dark panoramax-close">Fermer</button></div>';
		document.body.appendChild(dialog);
		dialog.querySelector('.panoramax-close').addEventListener('click', () => dialog.close());
		// click on the backdrop closes it
		dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
		// stop the viewer once closed
		dialog.addEventListener('close', () => { dialog.querySelector('iframe').src = 'about:blank'; });
	}
	return dialog;
}

/**
 * Open the Panoramax viewer on a picture, in a popup over the page
 */
export function openViewer(picture) {
	const d = getDialog();
	d.querySelector('iframe').src = picture.embedUrl;
	d.querySelector('.panoramax-open').href = picture.url;
	d.showModal();
}
