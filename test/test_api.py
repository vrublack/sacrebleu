# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import pytest

import sacrebleu

test_api_get_data = [
    ("wmt19", "de-en", 1, "Schöne Münchnerin 2018: Schöne Münchnerin 2018 in Hvar: Neun Dates", "The Beauty of Munich 2018: the Beauty of Munich 2018 in Hvar: Nine dates"),
    ("mtnt1.1/train", "ja-en", 10, "0歳から100歳の女性が登場する海外のスキンケアCM", "The overseas skin care commercial in which 0 to 100 year old females appear."),
    ("wmt19/google/ar", "en-de", 1, "Welsh AMs worried about 'looking like muppets'", "Walisische Abgeordnete befürchten als ,Idioten’ dazustehen."),
]

@pytest.mark.parametrize("testset, langpair, sentno, source, reference", test_api_get_data)
def test_api_get_source(testset, langpair, sentno, source, reference):
    with open(sacrebleu.get_source_file(testset, langpair)) as fh:
        line = fh.readlines()[sentno - 1].strip()

        assert line == source

@pytest.mark.parametrize("testset, langpair, sentno, source, reference", test_api_get_data)
def test_api_get_reference(testset, langpair, sentno, source, reference):
    with open(sacrebleu.get_reference_files(testset, langpair)[0]) as fh:
        line = fh.readlines()[sentno - 1].strip()
        assert line == reference

def test_api_get_available_testsets():
    available = sacrebleu.get_available_testsets()
    assert "wmt19" in available
    assert "wmt05" not in available

    available = sacrebleu.get_available_testsets()
    for testset in sacrebleu.DATASETS.keys():
        assert testset in available
        assert "slashdot_" + testset not in available

def test_api_get_langpairs_for_testset():
    for testset in sacrebleu.DATASETS.keys():
        available = sacrebleu.get_langpairs_for_testset(testset)
        for langpair in filter(lambda x: "-" in x, sacrebleu.DATASETS[testset].keys()):
            assert langpair in available
            assert "slashdot_" + langpair not in available