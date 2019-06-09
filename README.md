# Dash docset for Tensorflow.js

![screenshot](/screenshot.png)

View TensorFlow docs in the [dash](https://kapeli.com/dash)/[zeal](https://github.com/zealdocs/zeal) offline docset browser.

To use, you can add this feed in Dash/Zeal:
```
https://raw.githubusercontent.com/mnmly/dash-docset-tfjs/master/TensorFlow-js.xml
```
Or download the latest release [here](https://github.com/mnmly/dash-docset-tfjs/releases).

## Steps to generate the docset
+ Install [dashing](https://github.com/technosophos/dashing): `go get -u github.com/technosophos/dashing`
+ `pip install --user python-magic beautifulsoup4 lxml  python-magic-bin`
+ `make build`
+ `make install`

Right now this `dashing.json` only roughly parses function names (which is enough for most use cases).
Feel free to add more features and contribute!
