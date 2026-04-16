"""Robot Lost pygame MVP。

操作鍵:
- L / R / F: 對目前機器人執行一步
- N: 新機器人（保留 scent）
- C: 清除 scent
- B: 回放目前機器人歷史
- G: 匯出 replay.gif（需 Pillow）
- ESC: 離開
"""

from __future__ import annotations

import sys
from pathlib import Path

from robot_core import DIRECTIONS, RobotState, apply_instruction, matrix_snapshot


CELL = 64
PADDING = 40
HUD_HEIGHT = 120
WORLD_W = 5
WORLD_H = 3
WINDOW_W = PADDING * 2 + CELL * (WORLD_W + 1)
WINDOW_H = PADDING * 2 + CELL * (WORLD_H + 1) + HUD_HEIGHT


def export_replay_gif(frames, output_path: Path) -> bool:
    """嘗試輸出 GIF，若 Pillow 不存在則回傳 False。"""
    try:
        from PIL import Image
    except Exception:
        return False

    if not frames:
        return False

    pil_frames = []
    for surf in frames:
        raw = surf.get_buffer().raw
        size = surf.get_size()
        img = Image.frombytes("RGBA", size, raw)
        pil_frames.append(img.convert("P"))

    pil_frames[0].save(
        output_path,
        save_all=True,
        append_images=pil_frames[1:],
        duration=150,
        loop=0,
    )
    return True


def draw_robot(pygame, screen, state: RobotState):
    cx = PADDING + state.x * CELL + CELL // 2
    cy = PADDING + (WORLD_H - state.y) * CELL + CELL // 2

    if state.direction == "N":
        pts = [(cx, cy - 18), (cx - 14, cy + 14), (cx + 14, cy + 14)]
    elif state.direction == "E":
        pts = [(cx + 18, cy), (cx - 14, cy - 14), (cx - 14, cy + 14)]
    elif state.direction == "S":
        pts = [(cx, cy + 18), (cx - 14, cy - 14), (cx + 14, cy - 14)]
    else:
        pts = [(cx - 18, cy), (cx + 14, cy - 14), (cx + 14, cy + 14)]

    color = (220, 70, 70) if state.lost else (40, 130, 230)
    pygame.draw.polygon(screen, color, pts)


def render(pygame, screen, font, state, scents, status):
    screen.fill((245, 247, 252))

    # 畫地圖格線
    for gx in range(WORLD_W + 1):
        for gy in range(WORLD_H + 1):
            x = PADDING + gx * CELL
            y = PADDING + (WORLD_H - gy) * CELL
            rect = pygame.Rect(x, y, CELL, CELL)
            pygame.draw.rect(screen, (60, 70, 90), rect, 1)

    # 畫 scent
    for sx, sy, _dir in scents:
        x = PADDING + sx * CELL + CELL // 2
        y = PADDING + (WORLD_H - sy) * CELL + CELL // 2
        pygame.draw.circle(screen, (230, 140, 30), (x, y), 6)

    draw_robot(pygame, screen, state)

    hud_top = PADDING + CELL * (WORLD_H + 1) + 14
    texts = [
        f"目前: {state.x} {state.y} {state.direction}{' LOST' if state.lost else ''}",
        f"scent 數量: {len(scents)}",
        "按鍵: L/R/F 執行, N 新機器人, C 清 scent, B 回放, G 匯出GIF, ESC 離開",
        status,
    ]

    for i, line in enumerate(texts):
        surf = font.render(line, True, (20, 30, 50))
        screen.blit(surf, (PADDING, hud_top + i * 24))


def main():
    try:
        import pygame
    except Exception:
        print("請先安裝 pygame：pip install pygame")
        raise

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Week03 Robot Lost")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("microsoftjhengheiui", 20)

    state = RobotState(0, 0, "N")
    scents: set[tuple[int, int, str]] = set()
    history = [RobotState(state.x, state.y, state.direction, state.lost)]
    frames = []
    status = "準備開始"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

                if event.key == pygame.K_n:
                    state = RobotState(0, 0, "N")
                    history = [RobotState(state.x, state.y, state.direction, state.lost)]
                    status = "已建立新機器人（保留 scent）"

                elif event.key == pygame.K_c:
                    scents.clear()
                    status = "已清除 scent"

                elif event.key in (pygame.K_l, pygame.K_r, pygame.K_f):
                    cmd = {
                        pygame.K_l: "L",
                        pygame.K_r: "R",
                        pygame.K_f: "F",
                    }[event.key]
                    apply_instruction(state, cmd, WORLD_W, WORLD_H, scents)
                    history.append(RobotState(state.x, state.y, state.direction, state.lost))
                    status = f"執行指令: {cmd}"

                elif event.key == pygame.K_b:
                    for past in history:
                        render(pygame, screen, font, past, scents, "回放中...")
                        pygame.display.flip()
                        clock.tick(6)
                    status = "回放完成"

                elif event.key == pygame.K_g:
                    out = Path(__file__).parent / "assets" / "replay.gif"
                    ok = export_replay_gif(frames, out)
                    status = f"GIF 已輸出: {out.name}" if ok else "無法輸出 GIF（需 Pillow）"

        render(pygame, screen, font, state, scents, status)

        # 額外加分：可觀察 10x10 內部狀態快照（此處僅計算，方便擴充）。
        _ = matrix_snapshot(WORLD_W, WORLD_H, state)

        frames.append(screen.copy())
        if len(frames) > 180:
            frames.pop(0)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
