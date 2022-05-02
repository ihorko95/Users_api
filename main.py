from fastapi import FastAPI
import users.main


app = FastAPI(docs_url="/",
              title="User API",
              version="1.0"
              )
app.include_router(users.main.db)
app.include_router(users.main.router)



