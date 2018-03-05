// Copyright 2018 TomorrowData Srl
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


(function (window) {
  'use strict';

  var ws;
  var entryTpl = document.createElement("p");
  entryTpl.appendChild(document.createElement("span"));
  entryTpl.appendChild(document.createElement("span"));
  entryTpl.appendChild(document.createElement("span"));


  var onMessage = function(msg) {
    console.log(msg);
    var box = document.getElementById("message-container");
    box.insertBefore(buildNode(msg), box.firstChild);
  };

  var buildNode = function(msg) {
    var entry = entryTpl.cloneNode(true);
    entry.children[0].textContent = "device: " + msg.device;
    entry.children[1].textContent = msg.deviceTimestamp;
    entry.children[2].textContent = JSON.stringify(msg.payload);
    return entry;
  };

  var onConnectionOpen = function(){
    ws.addEventListener("message", function(event) {
      // Get the msg and parse JSON
      var msg = JSON.parse(event.data);
      onMessage(msg);
    });
  };

  var connectWS = function(){
    ws = new WebSocket(((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + "/ws");
    ws.addEventListener("open", function(event) {
      onConnectionOpen();
    });

    ws.addEventListener("error", function(err) {
      console.log(err);
      // There was a problem connecting to the WS
      setTimeout(function () {
        // reconnect after 2 sec.
        connectWS();
      }, 2000);
    });
  };

  document.addEventListener("DOMContentLoaded", function(event) { 
    connectWS();
  });

}(window));
