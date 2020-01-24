
import json
import openeo
from openeo.rest.imagecollectionclient import ImageCollectionClient


def vito_script(input_data, output_filename):
    """
    
    """

    backend_url = 'https://openeo.vito.be/openeo/0.4.2'
    
    if input_data == 'L1C':
        collection_id = 'SENTINEL2_L1C_SENTINELHUB'
    elif input_data == 'L2A':
        collection_id = 'SENTINEL2_L2A_SENTINELHUB'

    session = openeo.connect(backend_url)

    minx = 11.279182434082033
    maxx = 11.406898498535158
    maxy = 46.522729291844286
    miny = 46.464349400461145
    epsg = "EPSG:4326"
    spatial_extent = {'west':minx,'east':maxx,'north':maxy,'south':miny,'crs':epsg}

    temporal_extent=["2018-06-04T00:00:00.000Z","2018-06-22T00:00:00.000Z"]

    spectral_extent = ["B08", "B04", "B02"]

    s2_radiometry = ImageCollectionClient.load_collection(
                        session=session,
                        collection_id=collection_id,
                        temporal_extent=temporal_extent,
                        spatial_extent=spatial_extent
                        )

    B02 = s2_radiometry.band(spectral_extent[2])
    B04 = s2_radiometry.band(spectral_extent[1])
    B08 = s2_radiometry.band(spectral_extent[0])

    evi_cube = (2.5 * (B08 - B04)) / ((B08 + 6.0 * B04 - 7.5 * B02) + 1.0)

    min_evi = evi_cube.min_time()

    output = min_evi.download(output_filename,format="GeoTiff")
