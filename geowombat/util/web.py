import os
import wget
from datetime import datetime
from collections import namedtuple

from ..errors import logger

import pandas as pd


def _parse_google_filename(filename, landsat_parts, sentinel_parts, public_url):

    FileInfo = namedtuple('FileInfo', 'url url_file meta angles')

    file_info = FileInfo(url=None, url_file=None, meta=None, angles=None)

    f_base, f_ext = os.path.splitext(filename)

    fn_parts = f_base.split('_')

    if fn_parts[0].lower() in landsat_parts:

        # Collection 1
        url_ = '{PUBLIC}-landsat/{SENSOR}/01/{PATH}/{ROW}/{FDIR}'.format(PUBLIC=public_url,
                                                                         SENSOR=fn_parts[0],
                                                                         PATH=fn_parts[2][:3],
                                                                         ROW=fn_parts[2][3:],
                                                                         FDIR='_'.join(fn_parts[:-1]))

        url_filename = '{URL}/{FN}'.format(URL=url_, FN=filename)
        url_meta = '{URL}/{FN}_MTL.txt'.format(URL=url_, FN='_'.join(fn_parts[:-1]))
        url_angles = '{URL}/{FN}_ANG.txt'.format(URL=url_, FN='_'.join(fn_parts[:-1]))

        file_info = FileInfo(url=url_,
                             url_file=url_filename,
                             meta=url_meta,
                             angles=url_angles)

    # elif fn_parts[0].lower() in sentinel_parts:
    #
    #     safe_dir = '{SENSOR}_{M}{L}_'.format(SENSOR=fn_parts[0], M=fn_parts[2], L=fn_parts[3])
    #
    #     '/01/K/AB/S2A_MSIL1C_20160519T222025_N0202_R029_T01KAB_20160520T024950.SAFE/GRANULE/S2A_OPER_MSI_L1C_TL_SGS__20160519T234326_A004745_T01KAB_N02.02/IMG_DATA/S2A_OPER_MSI_L1C_TL_SGS__20160519T234326_A004745_T01KAB_B05.jp2'
    #
    #     fn = '{PUBLIC}-sentinel-2/tiles/{UTM}/{LAT}/{GRID}'.format(PUBLIC=public_url,
    #                                                                UTM=,
    #                                                                LAT=,
    #                                                                GRID=)

    return file_info


class Downloads(object):

    def __init__(self):

        self.gcp_public = 'https://storage.googleapis.com/gcp-public-data'

        self.landsat_parts = ['le07', 'lt05', 'lc08']
        self.sentinel_parts = ['s2a']

    def download_landsat_range(self, sensors, bands, path_range, row_range, date_range, **kwargs):

        """
        Downloads Landsat data from iterables

        Args:
            sensors (str): A list of sensors to download.
            bands (str): A list of bands to download.
            path_range (iterable): A list of paths.
            row_range (iterable): A list of rows.
            date_range (iterable): A list of ``datetime`` objects or a list of strings as yyyymmdd.
            kwargs (Optional[dict]): Keyword arguments to pass to ``download``.

        Examples:
            >>> from geowombat.util import download_landsat_range
            >>>
            >>> download_landsat_range(['lc08'], ['b4'], [42], [34], ['20170616', '20170620'])
        """

        if (len(date_range) == 2) and not isinstance(date_range[0], datetime):

            start_date = date_range[0]
            end_date = date_range[1]

            sdt = datetime.strptime(start_date, '%Y%m%d')
            edt = datetime.strptime(end_date, '%Y%m%d')

            date_range = pd.date_range(start=sdt, end=edt).to_pydatetime().tolist()

        for sensor in sensors:
            for band in bands:
                for path in path_range:
                    for row in row_range:
                        for dt in date_range:

                            str_date = '{:d}{:02d}{:02d}'.format(dt.year, dt.month, dt.day)

                            # TODO: check if L1TP is used for all sensors
                            # TODO: fixed DATE2
                            filename = '{SENSOR}_L1TP_{PATH:03d}{ROW:03d}_{DATE}_{DATE2}_01_T1_{BAND}.TIF'.format(SENSOR=sensor.upper(),
                                                                                                                  PATH=path,
                                                                                                                  ROW=row,
                                                                                                                  DATE=str_date,
                                                                                                                  DATE2=None,
                                                                                                                  BAND=band)

                            self.download(filename, **kwargs)

    def download(self, filename, outdir='.', from_google=True, metadata=True, overwrite=False):

        """
        Downloads an individual file

        Args:
            filename (str): The file to download.
            outdir (Optional[str]): The output directory.
            from_google (Optional[bool]): Whether to download from Google Cloud storage
            metadata (Optional[bool]): Whether to download metadata files.
            overwrite (Optional[bool]): Whether to overwrite an existing file.

        https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/042/034/LC08_L1TP_042034_20170616_20170629_01_T1/LC08_L1TP_042034_20170616_20170629_01_T1_B4.TIF

        Examples:
            >>> from geowombat.util import download
            >>>
            >>> # Download band 4 from Google Cloud storage to the current directory
            >>> download('LC08_L1TP_042034_20170616_20170629_01_T1_B4.TIF')

        Returns:
            None
        """

        if from_google:

            file_info = _parse_google_filename(filename,
                                               self.landsat_parts,
                                               self.sentinel_parts,
                                               self.gcp_public)

            file_on_disc = os.path.join(outdir, file_info.url_file)

            if file_info.url:

                if overwrite:

                    if os.path.isfile(file_on_disc):
                        os.remove(file_on_disc)

                if os.path.isfile(file_on_disc):
                    logger.warning('  The file already exists.')
                else:

                    wget.download(file_info.url_file, out=outdir)

                    if metadata:

                        wget.download(file_info.meta, out=outdir)
                        wget.download(file_info.angles, out=outdir)