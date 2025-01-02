from fastapi.responses import FileResponse


async def get_file_report(file: str,type:str):
    return FileResponse('file_report/'+type+'/'+file)