def sort_blocks(blocks):
    return sorted(blocks, key=lambda b: b.get('priority', 0), reverse=True)