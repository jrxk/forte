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
"""
Unit tests for dictionary word replacement data augmenter.
"""

import unittest
from forte.data.data_pack import DataPack
from ft.onto.base_ontology import Sentence

from forte.processors.data_augment.algorithms.back_translation_augmenter \
    import MarianMachineTranslator
from forte.processors.data_augment.algorithms.back_translation_augmenter \
    import BackTranslationAugmenter


class TestBackTranslationAugmenter(unittest.TestCase):
    def setUp(self):
        self.bta = BackTranslationAugmenter(
            model_to=MarianMachineTranslator(),
            model_back=MarianMachineTranslator(),
            configs={
                "src_language": "en",
                "tgt_language": "fr",
            }
        )

    def test_augmenter(self):
        data_pack = DataPack()
        text = "Natural Language Processing has never been made this simple!"
        data_pack.set_text(text)
        sent = Sentence(data_pack, 0, len(text))
        data_pack.add_entry(sent)

        translated_text = "The treatment of natural language has never been easier!"
        assert(translated_text == self.bta.augment(sent))


if __name__ == "__main__":
    unittest.main()
