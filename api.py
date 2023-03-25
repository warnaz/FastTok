import shutil
from typing import List
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Request, UploadFile, Form
from schemas import UploadVideo, GetVideo, GetListVideo
from models import Video, User
from services import open_file, save_video, write_video
from fastapi.responses import StreamingResponse, HTMLResponse
from starlette.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.post('/')
async def upload_video(
    back_tasks: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...)
):
    user = await User.objects.first()
    return await save_video(user, file, title, description, back_tasks)


# ormar использует pydantic, поэтому в документации будет показана структура json, которую мы ожидаем
@router.post('/video')
async def create_video(video: Video):
    await video.save()
    return video


@router.get('/show_video/list/{pk}', response_model=List[GetListVideo])
async def show_video(pk: int):
    video_list = await Video.objects.filter(user=pk).all()
    return video_list


@router.get('/index/{video_pk}', response_class=HTMLResponse)
async def index_video(request: Request, video_pk: int):
    return templates.TemplateResponse('index.html', {'request': request, 'path': video_pk})


@router.get("/video/{video_pk}")
async def get_streaming_video(request: Request, video_pk: int) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response
