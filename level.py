from objects import Block


def build_platforms(block_size, screen_height) -> tuple:
    platforms = []
    pattern = [("single", 1), ("platform", 5), ("single_down", 1), ("double_up", 2)]

    x = block_size * 5
    while len(platforms) < 25:
        for kind, n in pattern:
            if kind == "single":
                platforms.append(Block(x, screen_height - block_size * 3, block_size))
                x += block_size * 1.5
            elif kind == "platform":
                for i in range(n):
                    platforms.append(
                        Block(
                            x + i * block_size,
                            screen_height - block_size * 4,
                            block_size,
                        )
                    )
                x += block_size * (n + 1.5)
            elif kind == "single_down":
                platforms.append(Block(x, screen_height - block_size * 1, block_size))
                x += block_size * 2
            elif kind == "double_up":
                platforms.append(Block(x, screen_height - block_size * 4, block_size))
                platforms.append(
                    Block(x + block_size, screen_height - block_size * 4, block_size)
                )
                x += block_size * 2
    return platforms, x
