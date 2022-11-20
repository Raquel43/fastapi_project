#imports
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request, Response,status
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, Cookie, Depends
from starlette.responses import RedirectResponse, Response
import datetime,time

#MongoDB Connection info
client = MongoClient("mongodb+srv://raquel:libelula46@cluster0.5ilbxxp.mongodb.net")

#Database
bike_db = client['rental2']
#Collection
bike_collection = bike_db['bikes']

#Model
class Bike(BaseModel):
     id: int
     model: str
     brand: str
     features: str 
     year: int 
     size: str 
     availability: bool
     Price_day: list 
     location_latitude: float
     location_length: float
     image: str
    
    

#Initialize
app = FastAPI()

#Static file serv
app.mount("/static", StaticFiles(directory="static"), name="static")
#Jinja2 Template directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/bike/{id}", response_class=HTMLResponse)
def read_bike(request: Request, id: int):
    print(f'find bike called with id :{id}')
    result = bike_collection.find_one({'id': id})
    print(result['model'])
    return templates.TemplateResponse("view_bike.html", {"request": request, "bike": result})

@app.get("/bike", response_class=HTMLResponse)
def read_all_bike(request: Request):
    result = bike_collection.find({})
    print(result)
    return templates.TemplateResponse("index.html", {"request": request, "bike_list": result})

@app.get("/createui", response_class=HTMLResponse)
async def create_bike_ui(request: Request):
    return templates.TemplateResponse("new_bike.html", {"request": request})


@app.post("/create",response_class=HTMLResponse)

def create_bike(request:Request,id:int = Form(...), model:str = Form(...),brand:str = Form(...),features:str = Form(...),year:int = Form(...),size:int = Form(...), availability:bool = Form(...), Price_day:list = Form(...), location_latitude: float= Form(...), location_length: float=Form(...), image: str=Form(...)):
    print(f'id :{int(id)} model: {str(model)} brand:{str(brand)} features: {str(features)} year: {int(year)} size: {str(size)}, availability: {bool(availability)} Price_day: {str(Price_day)} location_latitude: {str(location_latitude)}, location_length {str(location_length)}')
    #initialize the model
    
    bike = Bike(id=id,model=model,brand=brand,features=features,year=year,size=size, availability=availability, Price_day=Price_day, location_latitude=location_latitude, location_length=location_length, image=image)
    print(str(bike.dict()))
    bike = jsonable_encoder(bike)
    bike_collection.insert_one(bike)
    print(" Bike added : now db id " + str(id))
    time.sleep(1)
    result = bike_collection.find({})
    return templates.TemplateResponse("index.html", {"request": request, "bike_list": result})


@app.get("/bike/delete/{id}",response_class=HTMLResponse)
def delete_bike(id:int,request:Request):
    print(" delete bike method called :"+str(id))
    result = bike_collection.delete_one({'id':id})
    time.sleep(1)
    result = bike_collection.find({})
    print(result)
    return templates.TemplateResponse("index.html", {"request": request, "bike_list": result})

@app.get("/bike/edit/{id}",response_class=HTMLResponse)
def edit_bike(id:int,request:Request):
    print(" method called :"+str(id))
    result = bike_collection.find_one({'id':id})
    return templates.TemplateResponse("edit_bike.html", {"request": request, "bike": result})

@app.post("/update",response_class=HTMLResponse)
def update_bike(request:Request,id:int = Form(...), model:str = Form(...),brand:str = Form(...),features:str = Form(...),year:int = Form(...),size:str = Form(...), availability:bool = Form(...), Price_day:list = Form(...), location_latitude: float= Form(...), location_length: float=Form(...), image: str=Form(...)):
    print('id :'+str(id))
    print('model '+str(model))
    print('brand ' + str(brand))
    print('features ' + str(features))
    print('year ' + str(year))
    print('size ' + str(size))
    print('availability ' + str(availability))
    print('Price_day ' + str(Price_day))
    print('location_latitude ' + str(location_latitude))
    print('location_length ' + str(location_length))
    print('image' + str(image))
    #initialize the model
    bike = Bike(id=id,model=model,brand=brand,features=features,year=year,size=size, availability=availability, Price_day=Price_day, location_latitude=location_latitude, location_length=location_length, image=image)
    print(str(bike.dict()))
    #call internal api
    update_api(bike)
    time.sleep(1)
    #get the updated list
    result = bike_collection.find({})
    print(str(result))
    return templates.TemplateResponse("index.html", {"request": request, "bike_list": result})


@app.put("/updateapi",status_code=202)
def update_api(bike:Bike):
    print('Update api called....'+str(bike.model))
    result = bike_collection.update_one({'id':bike.id},{"$set" : {'model':bike.model,'brand':bike.brand, 'features':bike.features, 'year':bike.year, 'size':bike.size, 'availability':bike.availability,'Price_day':bike.Price_day, 'location_latitude': bike.location_latitude, 'location_length': bike.location_length, 'image': bike.image}})
    return "UPDATE SUCCESS"

