

async function sendDatosToServer(url, typeSubmit, formData) {
  let datos;
  await Swal.fire({
    title: 'Procesando...', toast: true, showConfirmButton: false,
    showCancelButton: false, allowEscapeKey: false,
    didOpen: (resp) => {
      Swal.showLoading();
      fetch(url, {
        method: typeSubmit, body: formData
        , headers: {
          'Authorization': 'Bearer ' + getToken()
        }
      }).then((response) => {
        if (response.status === 401) { // 401 Unauthorized indica que la sesión ha expirado
          alert("Se ha agotado el tiempo de inicio de sesión. Serás redirigido a la página de inicio de sesión.");
          datos = {};
          Object.assign(datos, { 'resp_status': response.status, 'resp_statusText': response.statusText });
          // Extraer la URL base antes de "/api/"
          let posicionApi = url.indexOf("/api/");
          let url_modulo = url.substring(0, posicionApi);
          location.replace(url_modulo);
          // return datos;
        } else {
          response.json().then((data) => {
            Object.assign(data, { 'resp_status': response.status, 'resp_statusText': response.statusText });
            datos = data; Swal.close();
          });
        }
      }).catch((err) => {
        console.log(`DEV: Ctrl+shift+i, (Tab Red), click en la petición ${url}, Tab Respuesta`);
        // console.log(err);
        // Object.assign(datos, {'resp_status':response.status, 'resp_statusText': response.statusText});
        // datos = err; 
        Swal.close();
      });
    } //didOpen
  });
  return datos;
}

async function showMsg(iconGiven, titleGiven, msgGiven, timerGiven) {
  await Swal.fire({
    icon: iconGiven, title: titleGiven, text: msgGiven
    , timer: timerGiven, timerProgressBar: true, showCloseButton: true
  })
    .then((result) => {
      return true;
    });
}

async function showError(iconGiven, titleGiven, resp, timerGiven) {
  msgGiven = resp && resp.errormsg ? `${resp.errormsg}` : "";

  if (resp == undefined) {
    await Swal.fire({
      icon: iconGiven, title: 'Se presentaron algunos errores inesperados'
      , didOpen: (resp) => {
        Swal.showValidationMessage('Informelo al equipo de desarrollo');
      }
    }).then((result) => {
      return true;
    });
  } else {
    if (resp.resp_status >= 300) {
      await Swal.fire({
        icon: iconGiven, title: ''
        , didOpen: (resp) => {
          Swal.showValidationMessage(msgGiven);
        }
      }).then((result) => {
        return true;
      });
    } else {
      acum_messages = "Se presentaron los errores siguientes: \n";
      if (resp.errors) {
        res = JSON.parse(JSON.stringify(resp.errors));
        for (key in res) {
          // console.log(key); console.log(res[key]);
          acum_messages += `Campo [${key}] =`;
          for (index in res[key]) {
            //console.log(key2); console.log(res[key][key2]);
            acum_messages += `${res[key][index]}. `
          }
        }
        msgGiven += " " + acum_messages;
      }
      await Swal.fire({
        icon: iconGiven, title: titleGiven, timer: timerGiven, timerProgressBar: true
        , didOpen: (resp) => {
          Swal.showValidationMessage(msgGiven);
        }
      }).then((result) => {
        return true;
      });
    }

  }

}


function isFormValid(formName) {
  $(`#${formName}`).addClass("was-validated");
  if (!$(`#${formName}`)[0].checkValidity()) {
    $(`#${formName} .invalid-feedback`).each(function () {
      if ($(this)[0].offsetParent) { return false; }
    }); return false;
  }
  return true;
}


async function setSelect(idObjSelect, urlObjSelect, paramsSelectUser, idObjSelectOption, multipleOptions = false, paramsAdicionales = "") {
  return new Promise((resolve) => {
    parent = $(idObjSelect).closest('.modal');
    // urlObjSelect = urlObjSelect + "?csrf_token=" + $(`#csrf_token`).val();
    var objSelect = $(idObjSelect).select2({
      width: '100%',
      dropdownParent: parent.length ? parent : $(idObjSelect).parent(),
      multiple: multipleOptions,
      allowClear: true,
      placeholder: { id: '-1', text: 'Elija una opción' },
      ajax: {
        url: urlObjSelect + '?' + paramsAdicionales,
        dataType: "json",
        delay: 250,
        theme: "bootstrap-5",
        data: function (params) {
          return {
            q: params.term, // search term
            // csrf_token: $(`#csrf_token`).val(),
          };
        },
        processResults: function (data, params) {
          let jsonObj = [];
          // jsonObj.push({ 'id': '-1', 'text':'Elija una opción' });
          data.data.forEach(data => {
            let item = {};
            item['id'] = data[0];
            item['text'] = data[1];
            if (data[2] && data[2] != null) {
              item['disabled'] = true
            }
            jsonObj.push(item);
          });
          return { results: jsonObj };
        },
      },
      // minimumInputLength: 1,
    });
    // asignación del valor
    if ($(idObjSelect).find("option[value='" + idObjSelectOption + "']").length) {
      $(idObjSelect).val(idObjSelectOption).trigger('change');
    } else if (idObjSelectOption == "-1" || idObjSelectOption == "") {
      $(idObjSelect).val(null).trigger('change');
    } else {
      // simbolo = "?";
      // if (urlObjSelect.indexOf("?") >= 0) {
      //     simbolo = "&";
      // }
      $.ajax({
        // type: urlTypeAjax,
        url: urlObjSelect + "?" + paramsSelectUser + '=' + idObjSelectOption + '&' + paramsAdicionales,
        //contentType:'application/json',
        //data: stringifyData,
        data: function (params) {
          return {
            q: params.term, // search term
            // csrf_token: $(`#csrf_token`).val(),
          };
        },
      }).then(function (res) {
        let jsonObj = [];
        res.data.forEach(data => {
          let item = {};
          item['id'] = data[0];
          item['text'] = data[1];
          jsonObj.push(item);
          var option = new Option(data[1], data[0], true, true);
          objSelect.append(option);
        });
        objSelect.trigger('change');
      });
    }
    setTimeout(() => {
      resolve(true);
    }, 350);
  });
}


function fnRefreshTable(idTabla) {
  $(idTabla).DataTable().ajax.reload();
}

function fnExportTableToExcel(idTabla, filename2 = '') {
  var tab = document.getElementById(idTabla); // ID de la tabla
  var wb = XLSX.utils.table_to_book(tab, { sheet: "Sheet1" });

  var wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'binary' });
  // Obtener la fecha y hora actual
  var fechaHoraActual = new Date();
  // Obtener la fecha y hora en un formato personalizado
  var dia = fechaHoraActual.getDate();
  var mes = fechaHoraActual.getMonth() + 1; // Los meses van de 0 a 11
  var anio = fechaHoraActual.getFullYear();
  var horas = fechaHoraActual.getHours();
  var minutos = fechaHoraActual.getMinutes();
  var segundos = fechaHoraActual.getSeconds();

  // Formatear la fecha y la hora en el formato deseado (por ejemplo, "DD/MM/AAAA HH:MM:SS")
  var fechaHoraFormateada = anio + '-' + mes + '-' + dia + ' ' + horas + '_' + minutos + '_' + segundos;

  function s2ab(s) {
    var buf = new ArrayBuffer(s.length);
    var view = new Uint8Array(buf);
    for (var i = 0; i < s.length; i++) {
      view[i] = s.charCodeAt(i) & 0xFF;
    }
    return buf;
  }

  var blob = new Blob([s2ab(wbout)], { type: 'application/octet-stream' });
  var filename = filename2 + '_' + fechaHoraFormateada + '.xlsx';

  if (navigator.msSaveBlob) {
    // Para Internet Explorer y Microsoft Edge
    navigator.msSaveBlob(blob, filename);
  } else {
    // Para otros navegadores
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.target = '_blank';
    link.dispatchEvent(new MouseEvent('click'));
  }
}

function resetModalGeneric(formDado, idObjModal, hideModal = false) {
  $(`#${formDado}`).removeClass("was-validated"); $(`#${formDado}`).trigger('reset');
  $(`#${formDado} #id`).val("");

  if (hideModal == true) {
    $(`#${idObjModal}`).modal("hide");
  }
}

// empleado para datatables en general

$.fn.dataTable.ext.buttons.reload = {
  className: 'buttons-alert',
  text: 'Recargar',
  action: function (e, dt, node, config) {
    //dt.clear().draw(); // opcional
    dt.ajax.reload();
  }
};

function getToken() {
  // Obtener el token JWT
  return localStorage.getItem('jwt-token');
}

// una opción mas par garantizar la eliminación del history:
//  https://www.cluemediator.com/how-to-disable-the-browser-back-button-using-javascript
function disableBack() { window.history.forward(); }
// setTimeout("disableBack()", 0);
window.onunload = function () { null };
