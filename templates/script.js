
/* 假資料 */

const data = {

    taipei: [
        { name: "站點A", lat: 25.0416, lng: 121.5439 },
        { name: "站點B", lat: 25.0470, lng: 121.5170 },
        { name: "站點C", lat: 25.0330, lng: 121.5654 }
    ],

    taichung: [
        { name: "站點D", lat: 24.1477, lng: 120.6736 },
        { name: "站點E", lat: 24.1370, lng: 120.6860 }
    ],

    kaohsiung: [
        { name: "站點F", lat: 22.6273, lng: 120.3014 },
        { name: "站點G", lat: 22.6390, lng: 120.3020 }
    ]

};

// // 更改獲取產業別的清單，因為是從資料庫取，所以乾脆改成這個形式避免資料有出入
//         fetch('/Information/get_industry/')
//         .then(response => response.json())
//         .then(data => {
//             if (data.industrylist) {
//                 let sel2 = document.getElementById("datalistOptions-after");
//                 sel2.innerHTML = "";  // 清空舊的選項

//                 data.industrylist.forEach(industry => {
//                     let opt = document.createElement("option");
//                     opt.innerHTML = industry;
//                     sel2.appendChild(opt);
//                 });
//             }
//         })
//         .catch(error => {
//             console.error('傳送錯誤：', error);
//         });

/* 各城市中心 */

const cityCenter = {

    taipei: [25.0416, 121.5650],
    taichung: [24.1477, 120.6736],
    kaohsiung: [22.6273, 120.3014]

};

/* 初始化地圖 */

var map = L.map('map').setView([25.04, 121.55], 13);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
).addTo(map);

/* marker layer */

var markers = L.layerGroup().addTo(map);

/* 顯示城市 */

function showCity(city) {

    markers.clearLayers();

    let stations = data[city];

    let mode = document.getElementById("modeSelect").value;

    /* 建立 marker */

    let bounds = [];

    stations.forEach(function (s) {

        let marker = L.marker([s.lat, s.lng])
            .addTo(markers)
            .bindPopup(s.name);

        bounds.push([s.lat, s.lng]);

    });

    /* 法一：顯示全部點 */

    if (mode === "all") {

        let group = new L.featureGroup(markers.getLayers());
        map.fitBounds(group.getBounds());

    }

    /* 法二：固定中心 */

    if (mode === "center") {

        map.setView(cityCenter[city], 13);

    }

}

/* 初始顯示 */

showCity("taipei");

/* 事件 */

document.getElementById("citySelect")
    .addEventListener("change", function () {

        showCity(this.value);

    });

document.getElementById("modeSelect")
    .addEventListener("change", function () {

        let city = document.getElementById("citySelect").value;
        showCity(city);

    });