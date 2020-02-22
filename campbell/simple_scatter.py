from IPython.display import display, HTML

import pandas as pd
import panel as pn
from jinja2 import Template

from campbell.constants import ENV, TEMPLATE_DIR


class SimpleScatter:

    def __init__(self, df: pd.DataFrame, jupyter: bool):

        self.data = df.to_json(orient="index")

        self.is_jupyter = jupyter

        self.template = ENV.get_template("simple_scatter.html")

    def plot(self):
        #html = self.template.render()
        #tmpl = pn.Template(self.template)
        #return pn.pane.HTML(html)
        #return tmpl.servable()
        with open(TEMPLATE_DIR / "simple_scatter.html", "r") as f:
            html = f.read()
        return html



if __name__ == "__main__":
    from sklearn.datasets import load_boston

    bos = load_boston()
    df = pd.DataFrame(bos.data, columns=bos.feature_names)
    df = df.iloc[:20, :]

    app = SimpleScatter(df=df, jupyter=True)
    print(app.plot())