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
"""Read all data in IMDB and merge them to a csv file."""
import os
import csv

from forte.data.caster import MultiPackBoxer
from forte.data.multi_pack import MultiPack
from forte.data.readers import LargeMovieReader
from forte.pipeline import Pipeline
from forte.utils.utils_io import maybe_create_dir
from ft.onto.base_ontology import Document


def clean_web_text(st):
    """clean text."""
    st = st.replace("<br />", " ")
    st = st.replace("&quot;", "\"")
    st = st.replace("<p>", " ")
    if "<a href=" in st:
        while "<a href=" in st:
            start_pos = st.find("<a href=")
            end_pos = st.find(">", start_pos)
            if end_pos != -1:
                st = st[:start_pos] + st[end_pos + 1:]
            else:
                print("incomplete href")
                print("before", st)
                st = st[:start_pos] + st[start_pos + len("<a href=")]
                print("after", st)

        st = st.replace("</a>", "")
    st = st.replace("\\n", " ")
    # st = st.replace("\\", " ")
    # while "  " in st:
    #   st = st.replace("  ", " ")
    return st


def main():
    pipeline = Pipeline[MultiPack]()
    reader = LargeMovieReader()
    pipeline.set_reader(reader)
    pipeline.add(MultiPackBoxer())

    pipeline.initialize()

    dataset_path = "data/IMDB_raw/aclImdb/"
    input_file_path = {
        "train": os.path.join(dataset_path, "train"),
        "test": os.path.join(dataset_path, "test")
    }
    output_path = "data/IMDB/"
    maybe_create_dir(output_path)
    output_file_path = {
        "train": os.path.join(output_path, "train.csv"),
        "test": os.path.join(output_path, "test.csv")
    }
    set_labels = {
        "train": ["pos", "neg", "unsup"],
        "test": ["pos", "neg"],
    }

    for split in ["train", "test"]:
        with open(output_file_path[split], "w", encoding="utf-8")\
            as output_file:
            writer = csv.writer(output_file, delimiter="\t", quotechar="\"")
            writer.writerow(["content", "label", "id"])
            for label in set_labels[split]:
                data_packs = \
                    pipeline.process_dataset(
                        os.path.join(input_file_path[split], label))
                for pack in data_packs:
                    example_id = pack.get_pack('default').pack_name
                    for pack_name in pack.pack_names:
                        p = pack.get_pack(pack_name)
                        for doc in p.get(Document):
                            writer.writerow(
                                [clean_web_text(doc.text.strip()), label, example_id])


if __name__ == "__main__":
    main()
