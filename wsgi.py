from app import app
from icecream import ic

ic.disable()  # Disable globally all icecream breakpoints
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
