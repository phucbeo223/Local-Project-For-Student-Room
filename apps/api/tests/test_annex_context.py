from app.room_service.chatbot.annex_context import whole_annex_rows


def test_native_table_keeps_header_and_each_selected_whole_row():
    parent = 'Phụ lục II\nĐiều kiện áp dụng\n|TT|Loại hình|Nhóm 1|Nhóm 2|\n|1|Nhà chung cư, nhà ở tập|7 tầng|5 tầng|\n| |thể|3.000 m2|1.000 m2|\n|2|Trường học|5 tầng|3 tầng|\n|3|Khách sạn, dịch vụ lưu trú|7 tầng|5 tầng|\n| |khác|3.000 m2|1.000 m2|\n'
    result = whole_annex_rows(parent, 'Nhà trọ nhiều phòng', '')
    assert result['context_complete']
    assert '|TT|Loại hình|Nhóm 1|Nhóm 2|' in result['content']
    assert 'thể|3.000 m2|1.000 m2|' in result['content']
    assert 'khác|3.000 m2|1.000 m2|' in result['content']
    assert 'Trường học' not in result['content']
    for span in result['annex_source_spans']:
        assert parent[span['start']:span['end']] in result['content']


def test_plain_annex_keeps_conditions_and_rejects_over_budget():
    parent = 'Phụ lục I\nCó các điều kiện sau:\n 1. Nhà ở tập thể.\n 2. Trường học.\n 3. Cơ sở lưu trú cao từ 2 tầng\n hoặc diện tích 50 m2.\n'
    result = whole_annex_rows(parent, 'Phòng trọ', '')
    assert '2 tầng\n hoặc diện tích 50 m2' in result['content']
    assert whole_annex_rows(parent, 'Phòng trọ', '', limit=30) is None
    assert whole_annex_rows('Điều 3. Nghĩa vụ\n1. Nội dung', 'phòng trọ', '') is None
