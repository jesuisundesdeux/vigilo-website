/* Base maps (no API key needed), same as app.vigilo.city */
const ATTRIB_OSM = '&copy; <a href="https://www.openstreetmap.org/copyright">contributeurs OpenStreetMap</a>';

export function addBaseLayers(map) {
	const osmFr = L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
		maxZoom: 20, maxNativeZoom: 19, subdomains: 'abc',
		attribution: ATTRIB_OSM + ', tuiles <a href="https://www.openstreetmap.fr/">OSM France</a>'
	});
	const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 20, maxNativeZoom: 19, attribution: ATTRIB_OSM
	});
	const geopf = (layer, format) => L.tileLayer(
		'https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&STYLE=normal&TILEMATRIXSET=PM'
		+ '&LAYER=' + layer + '&FORMAT=' + format + '&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
		{ maxZoom: 20, maxNativeZoom: 18, attribution: '&copy; <a href="https://www.ign.fr/">IGN</a>' });
	const layers = {
		'OSM France': osmFr,
		'OpenStreetMap': osm,
		'Plan IGN': geopf('GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'image/png'),
		'Photos aériennes': geopf('ORTHOIMAGERY.ORTHOPHOTOS', 'image/jpeg')
	};
	osmFr.addTo(map);
	// OSM France unavailable: fall back on openstreetmap.org
	let loaded = false;
	osmFr.once('tileload', () => { loaded = true; });
	osmFr.on('tileerror', function onError() {
		if (!loaded && map.hasLayer(osmFr)) {
			osmFr.off('tileerror', onError);
			map.removeLayer(osmFr);
			osm.addTo(map);
		}
	});
	L.control.layers(layers, null, { position: 'topright' }).addTo(map);
	return layers;
}
