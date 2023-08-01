def test_markdown_index_about_page(markdown_index_client):
    resp = markdown_index_client.get("/about")
    assert resp.status_code == 200
    resp = markdown_index_client.get("/about/")
    assert resp.status_code == 404
    resp = markdown_index_client.get("/shop")
    assert resp.status_code == 404
