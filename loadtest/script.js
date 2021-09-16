import http from "k6/http";

export default function () {
  var url = "http://0.0.0.0:4000";

  var params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  http.get(url, params);
}
