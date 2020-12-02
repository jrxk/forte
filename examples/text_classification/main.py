# Copyright 2020 The Forte Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

from forte.models.imdb_text_classifier.model import IMDBClassifier
import config_data
import config_classifier


def main():
    model = IMDBClassifier(config_data, config_classifier)
    if not os.path.isfile("data/IMDB/train.pkl")\
            or not os.path.isfile("data/IMDB/eval.pkl")\
            or not os.path.isfile("data/IMDB/predict.pkl")\
            or not os.path.isfile("data/IMDB/unsup.pkl"):
        model.prepare_data("data/IMDB")
    # model.run(do_train=True, do_eval=True, do_test=False)
    model.run_uda(do_train=True, do_eval=True, do_test=False)


if __name__ == "__main__":
    main()