from staticjinja import make_renderer

if __name__ == '__main__':
    renderer = make_renderer()
    renderer.run(use_reloader=False)

