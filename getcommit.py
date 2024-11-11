import config

def gemini(msg):
    response = config.MODEL.generate_content(msg)
    return response




