#!/usr/bin/env python3
# coding=utf-8

import praw
import pytest

from bdfr.exceptions import SiteDownloaderError
from bdfr.site_downloaders.gallery import Gallery


@pytest.mark.online
@pytest.mark.parametrize(('test_ids', 'expected'), (
    ([
        {'media_id': '18nzv9ch0hn61'},
        {'media_id': 'jqkizcch0hn61'},
        {'media_id': 'k0fnqzbh0hn61'},
        {'media_id': 'm3gamzbh0hn61'},
    ], {
        'https://i.redd.it/18nzv9ch0hn61.jpg',
        'https://i.redd.it/jqkizcch0hn61.jpg',
        'https://i.redd.it/k0fnqzbh0hn61.jpg',
        'https://i.redd.it/m3gamzbh0hn61.jpg'
    }),
    ([
        {'media_id': '04vxj25uqih61'},
        {'media_id': '0fnx83kpqih61'},
        {'media_id': '7zkmr1wqqih61'},
        {'media_id': 'u37k5gxrqih61'},
    ], {
        'https://i.redd.it/04vxj25uqih61.png',
        'https://i.redd.it/0fnx83kpqih61.png',
        'https://i.redd.it/7zkmr1wqqih61.png',
        'https://i.redd.it/u37k5gxrqih61.png'
    }),
))
def test_gallery_get_links(test_ids: list[dict], expected: set[str]):
    results = Gallery._get_links(test_ids)
    assert set(results) == expected


@pytest.mark.online
@pytest.mark.reddit
@pytest.mark.parametrize(('test_submission_id', 'expected_hashes'), (
    ('m6lvrh', {
        '5c42b8341dd56eebef792e86f3981c6a',
        '8f38d76da46f4057bf2773a778e725ca',
        'f5776f8f90491c8b770b8e0a6bfa49b3',
        'fa1a43c94da30026ad19a9813a0ed2c2',
    }),
    ('ljyy27', {
        '359c203ec81d0bc00e675f1023673238',
        '79262fd46bce5bfa550d878a3b898be4',
        '808c35267f44acb523ce03bfa5687404',
        'ec8b65bdb7f1279c4b3af0ea2bbb30c3',
    }),
    ('nxyahw', {
        'b89a3f41feb73ec1136ec4ffa7353eb1',
        'cabb76fd6fd11ae6e115a2039eb09f04',
    }),
    ('obkflw', {
        '65163f685fb28c5b776e0e77122718be',
        '2a337eb5b13c34d3ca3f51b5db7c13e9',
    }),
))
def test_gallery_download(test_submission_id: str, expected_hashes: set[str], reddit_instance: praw.Reddit):
    test_submission = reddit_instance.submission(id=test_submission_id)
    gallery = Gallery(test_submission)
    results = gallery.find_resources()
    [res.download(120) for res in results]
    hashes = [res.hash.hexdigest() for res in results]
    assert set(hashes) == expected_hashes


@pytest.mark.parametrize('test_id', (
    'n0pyzp',
))
def test_gallery_download_raises_right_error(test_id: str, reddit_instance: praw.Reddit):
    test_submission = reddit_instance.submission(id=test_id)
    gallery = Gallery(test_submission)
    with pytest.raises(SiteDownloaderError):
        gallery.find_resources()
