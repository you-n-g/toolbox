from typer import Typer
from xytb.apps.codereview import review
app = Typer()


@app.command()
def placeholder():
    print("placeholder")

app.command()(review)
