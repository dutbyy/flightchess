from pyshow.src.render import ScreenProcessor

def pipeline(queue, config):
    import signal
    signal.signal(signal.SIGTERM, bye)

    try :
        range_x = config["range_x"]
        range_y = config["range_y"]
        display_size = config.get("display_size", [800, 600])
    except Exception as e:
        raise Exception("Please Point the Maps Limit and Display Size")

    pygame.init()
    windowSize = [800, 800] #generator.gen_winsize(config)      # 窗口大小处理
    screen = pygame.display.set_mode(display_size)    # 创建screen
    pygame.display.set_caption("PipeLine")          # 指定display的title

    bg_path = config.get("bg_img", None)
    try :
        bg_img = None if not bg_path else pygame.image.load(bg_path)
    except Exception as e:
        bg_img = None
        print(f"Load Back Image Failed! path: [{bg_path}]")

    tcolor = config.get("tcolor", black)
    fontsize = config.get("fontsize", 12)
     processor = ScreenProcessor(screen, range_x, range_y, display_size, tcolor, bg_img)

     old_obs, obs = None, None
     try:
         while True:
             for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     pygame.quit()
                 elif event.type == pygame.MOUSEBUTTONDOWN:
                     if event.button == 4:
                         processor.scale_magnify()
                     elif event.button == 5:
                         processor.scale_minify()
                     elif event.button == 1:
                         processor.mouse_moving = True
                 elif event.type == pygame.MOUSEBUTTONUP:
                     processor.mouse_moving = False

         #print('qsize is ', queue.qsize())
             if queue.qsize() > 30:
                 print(f"Render Delay, {queue.qsize()}")
             if queue and not queue.empty():
                 old_obs = obs
                 obs = queue.get()
             if not queue or not obs:
                 print("obs is None")
                 time.sleep(1)
                 continue
             processor.fix_screen_bg()
             processor.fix_move()
             processor.fix_screen_by_obs(obs)
             processor.fix_screen_by_mouse()
             pygame.display.flip()
             pygame.time.wait(1)
     except Exception as e:
         print('**'*10)
         print(e)
