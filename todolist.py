from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.task}. {self.deadline.strftime('%d %b')}"

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

while True:
    print("""1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit""")
    i = " "
    today = datetime.today()
    while i not in ("0123456"):
        i = input()
    i = int(i)
    if i == 0:
        print("Bye!")
        break
    elif i == 1:
        print(f"\nToday {today.strftime('%d %b')}:")
        rows = session.query(Table).filter(Table.deadline == today).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i]}")
    elif i == 2:
        for j in range(7):
            dd = today.date() + timedelta(days=j)
            print(f"\n{dd.strftime('%A %d %b')}:")
            rows = session.query(Table).filter(Table.deadline == dd).all()
            if len(rows) == 0:
                print("Nothing to do!")
            else:
                for i in range(len(rows)):
                    print(f"{i + 1}. {rows[i]}")
    elif i == 3:
        print("\nAll tasks:")
        rows = session.query(Table).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i]}")
    elif i == 4:
        print("\nMissed tasks:")
        rows = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if len(rows) == 0:
            print("Nothing is missed!")
        else:
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i]}")
    elif i == 5:
        tsk = input("\nEnter task\n")
        dln = input("Enter deadline\n")
        y, m, d = dln.split("-")
        dln = datetime(int(y), int(m), int(d))
        new_row = Table(task=tsk, deadline=dln)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    else:
        rows = session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print("Nothing to delete!")
        else:
            print("\nChose the number of the task you want to delete:")
            for i in range(len(rows)):
                print(f"{i + 1}. {rows[i]}")
            i = -1
            while i - 1 not in range(len(rows)):
                i = int(input())
            session.delete(rows[i - 1])
            session.commit()
            print("Task has been deleted!")
    print()