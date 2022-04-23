
/* 
 设置cookie
 */
function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  var expires = "expires=" + d.toGMTString();
  document.cookie = cname + "=" + cvalue + "; " + expires + ";" + "Path=/";
}

/* 
 获取cookie
 */
function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i].trim();
    if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
  }
  return "";
}

/*

*/
function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i].trim();
    if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
  }
  return "";
}

function requestParameter() {
  /*
    获取路由参数
   */
    var url = window.location.search; //获取url中"?"符后的字串
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        var strs = str.split("&");
        for (var i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = (strs[i].split("=")[1]);
        }
    }
    return theRequest
}

function myRequest(url, type, data, callback, async=true) {
  $.ajax({
    url: 'http://localhost:8000' + url,
    type: type,
    dataType: 'json',
    data: data,
    async: async,
    headers: {
      'Authorization': getCookie("token")
    },
    success: function (result) {
      console.log("code:" + result.code )
      try {
        layer.msg(result.msg)
      } catch(e) {
        console.log('layer is not defined')
        alert(result.msg)
      }
      if (result.code == 0) {
        callback(result)
      } else if (result.code == 401) {
        window.location.href = "../login/login.html";
      }
    },
    error: function (xhr, errorType, error) {
      alert('网络错误');
    }
  });
}
