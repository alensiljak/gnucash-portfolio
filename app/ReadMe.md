This folder contains the web application implemented in Flask. It is intended to be used as the full GUI for accepting user input (parameters) and displaying the output.

Considering several factors below, it might be preferrable to use an independent application to work with Portfolio. It would utilize gnucash database directly.

- Ease of development
Developing reports on gnucash_utilities stack seems fairly straightforward and simpler than Scheme, GnuCash reporting engine. The control of the output is also easier by directly editing HTML templates and styles.

- Performance
Comparing the output through GnuCash reports to the native output using Python stack (piecash + HTML output), the advantage is significantly on the side of Python components.

# Running

There are two ways to run the web app:

1. Run app.py
2. "run.py run"

The second is created so that the app can be debugged by Python extension for Visual Studio Code.
