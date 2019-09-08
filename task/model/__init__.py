# from keras.models import load_model
# import numpy as np
# import os
# from back_end import settings
# from . import e2emodel as model
# from . import grumodel as grum
# from . import grumodel as e2e
# print('load model...')
# model = load_model(os.path.join(settings.MODEL_DIR,'ocr_plate_all_w_rnn_2.h5'), compile=False)
# e2e.e2e.rnn = model.construct_model(os.path.join(settings.MODEL_DIR, "ocr_plate_all_w_rnn_2.h5"))
# e2e.e2e.gru = grum.construct_model(os.path.join(settings.MODEL_DIR, "ocr_plate_all_gru.h5"))
# print('load done.')