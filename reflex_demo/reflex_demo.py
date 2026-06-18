import reflex as rx
import sqlmodel as sql
from datetime import date, time, datetime

class Notes(rx.Model, table=True):
    content: str
    date: date
    time: time

class Query(rx.State):
    notes: list[Notes]

    @rx.event
    def query(self):
        with rx.session() as session:
            self.notes=session.exec(sql.select(Notes).order_by(sql.desc(Notes.id))).all()

class Insert(rx.State):
    @rx.event
    def insert(self, form_data: dict):
        date = datetime.now().date()
        time = datetime.now().time()

        form_data["date"]=date
        form_data["time"]=time

        with rx.session() as session:
            session.exec(sql.insert(Notes).values(**form_data))
            session.commit()

        yield Query.query()

class Remove(rx.State):  
    @rx.event
    def remove(self, note: str):
        with rx.session() as session:
            session.exec(sql.delete(Notes).where(Notes.content == note))
            session.commit()
        
        yield Query.query()

def form():
    return rx.form(
        rx.hstack(
            rx.input(placeholder="Add Notes...", name="content"),
            rx.button("Submit", type="submit"),
        ),
        on_submit=Insert.insert(),
        reset_on_submit=True,
    )

def showNote(note: Notes):
    return rx.hstack(
        rx.text(note.content),
        rx.spacer(),
        rx.form(
            rx.button("Remove", on_click=lambda: Remove.remove(note.content)),
        ),
    )

def index() -> rx.Component:
    return rx.center(
        rx.card(
            rx.heading("Notes"),
            form(),
            rx.center(
                rx.vstack(rx.foreach(Query.notes, showNote)),
            ),
            on_mount=Query.query,
        ),
        width="100%",
        height="100vh",
    )

app=rx.App()
app.add_page(index)