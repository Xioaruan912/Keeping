'''
作者: Xioaruan912 xioaruan@gmail.com
最后编辑人员: Xioaruan912 xioaruan@gmail.com
文件作用介绍: 
'''
from  mcp.server.fastmcp  import FastMCP
import httpx
from typing import Any


#快速构建MCPserver
mcp = FastMCP("weather",log_level = "ERROR")

NWS_API_BASE= "https://api.weather.gov"
User_Agent = "weather-app/1.o"

# 构建请求函数
async def make_nws_req(url : str ) -> dict[str,Any] | None:
    header = {
        "User-Agent": User_Agent,
        "Accept" : "application/geo+json"
        }
    async with httpx.AsyncClient() as client:
        try:
            response =  await client.get(url,headers=header,timeout = 30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
#构建工具
def format_alert(feature: dict) -> str:

    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


# 构建第一个tool
@mcp.tool()
async def get_alerts(state:str) -> str:
    """获取美国天气州
    
    Args:
    state ： 州的名称
    """
    #获取天气预报办公室
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_req(url=url)
    if not data or "features" not in data:  #检查调用是否成功
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:        #检查数据是否存在
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]   #格式化
    return "\n---\n".join(alerts)

#第二个tool 会通过下面 的 “”“”“” 中获取 mcp的描述传递给大模型
@mcp.tool()
async def get_forecast(latitude:float , longitude : float ) -> str:
    """获取美国天气 
    
    Args:
        latitude : 精度
        longitude : 纬度
    """
    #获取天气预报办公室
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_req(points_url)
    if not points_data:
        return "Unable to fetch forecast data for this location."
    #增加 data 传递
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_req(forecast_url)
    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    mcp.run(transport="stdio") #启动mcp server
    #使用  输入 输出
