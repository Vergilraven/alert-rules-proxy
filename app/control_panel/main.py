bufferingcloud_dashboard.include_router(admin.router, prefix="/api", tags=["管理接口"])
bufferingcloud_dashboard.include_router(user.router, prefix="/api/user", tags=["用户接口"])
bufferingcloud_dashboard.include_router(cursor.router, prefix="/api/cursor", tags=["Cursor API"])
bufferingcloud_dashboard.include_router(stock.router, prefix="/api/stock", tags=["股票数据"])

if __name__ == "__main__":
    uvicorn.run("app.control_panel.main:bufferingcloud_dashboard", host="0.0.0.0", port=8000, reload=True)