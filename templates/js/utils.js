
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

function myRequest(url, type, data, callback) {
  $.ajax({
    url: 'http://localhost:8000' + url,
    type: type,
    dataType: 'json',
    data: data,
    async: false,
    headers: {
      'Authorization': getCookie("token")
    },
    success: function (result) {
      console.log("code:" + result.code )
      try {
        layer.msg(result.msg)
      } catch(e) {
        console.log('layer is not defined')
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
