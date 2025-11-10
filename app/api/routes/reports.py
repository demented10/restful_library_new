from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from datetime import date
from app.services.report_service import ReportService
from app.api.dependencies import get_report_service

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/overdue")
def get_overdue_report(
    report_date: date = Query(..., description="Дата для отчета в формате YYYY-MM-DD"),
    format: str = Query("csv", pattern="^(csv|xlsx)$", description="Формат отчета: csv или xlsx"),
    service: ReportService = Depends(get_report_service),
):
    """
    Сгенерировать отчет о просроченных книгах
    
    - **report_date**: Дата, на которую проверять просрочку
    - **format**: Формат отчета (csv или xlsx)
    """
    try:
        report_data = service.create_overdue_report(report_date, format)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )

    # Определяем тип контента и расширение файла
    if format == "xlsx":
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_extension = "xlsx"
    else:
        media_type = "text/csv"
        file_extension = "csv"

    # Возвращаем файл как ответ
    return Response(
        content=report_data,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename=overdue_report_{report_date}.{file_extension}"
        }
    )