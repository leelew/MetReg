import os
import sys
sys.path.append('../../')


import numpy as np
from MetReg.data.data_generator import Data_generator
from MetReg.data.data_preprocessor import Data_preprocessor
from MetReg.utils.utils import save2pickle, _get_task_from_regions, _get_nan_mask


def main(X,
         y=None,
         intervel=18,
         out_path='/hard/lilu/ERA5_1981_2017_DD_A1/',
         out_file=''):

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    region = _get_task_from_regions(
        X.shape[-3], X.shape[-2], interval=intervel)

    for num_jobs, attr in enumerate(region):
        print('now processing jobs {}'.format(num_jobs))
        X_region = X[:, attr[0]:attr[0]+intervel, attr[1]:attr[1]+intervel, :]
        y_region = y[:, attr[0]:attr[0]+intervel, attr[1]:attr[1]+intervel, :]

        assert y_region.shape[-2] == 18 and y_region.shape[-3] == 18

        mask = _get_nan_mask(y_region[:, :, :, 0])

        # data preprocess
        dp = Data_preprocessor(X_region, y_region, normalize=True)
        X_region, y_region = dp()
        print('Parameters is setting as {}'.format(print(dp)))

        # data generator
        dg = Data_generator(X_region, y_region, len_inputs=10, window_size=15)
        data = dg()

        save2pickle(data, out_path, 'ERA5_DD_A1_case_'+str(num_jobs)+'.pickle')
        save2pickle(mask, out_path, 'nan_mask_case_'+str(num_jobs)+'.pickle')


if __name__ == "__main__":

    input_path = '/WORK/sysu_yjdai_6/hard/lilu/'
    st = np.load(input_path+'ERA5_1981_2017_DD_A1_st_lv1.npy')
    swv = np.load(input_path+'ERA5_1981_2017_DD_A1_swv_lv1.npy')
    mtpr = np.load(input_path+'ERA5_1981_2017_DD_A1_mtpr.npy')

    X = np.concatenate((swv, st, mtpr), axis=-1)
    y = swv

    del swv, st, mtpr

    main(X, y, out_path='/WORK/sysu_yjdai_6/hard/lilu/ERA5_1981_2017_DD_A1/')
