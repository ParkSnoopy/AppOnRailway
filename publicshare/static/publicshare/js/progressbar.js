
const fileinput = document.getElementById('fileuploadForm')
const filetitle = document.getElementById('titleForm')
const uploadBtn = document.getElementById('upload-btn')
const progressBox = document.getElementById('progress-box')
const csrftoken = document.getElementsByName('csrfmiddlewaretoken')

uploadBtn.addEventListener('click', () => {
	progressBox.style = "display:_;"
	uploadBtn.style = "display:none;"

	const filedata = fileinput.files[0]

	const fd = new FormData()
	fd.append('csrfmiddlewaretoken', csrftoken[0].value)
	fd.append('file', filedata)
	fd.append('title', filetitle)

	$.ajax({
		type: 'POST', 
		url: 'new/', 
		enctype: 'multipart/form-data', 
		data: fd, 
		beforeSend: function () {

		}, 
		xhr: function () {
			const xhr = new window.XMLHttpRequest()
			xhr.upload.addEventListener('progress', (e) => {
				const percent = ( 100 * e.loaded / e.total ).toFixed( 1 )
				progressBox.innerHTML = `
				<div class="progress">
				  <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100">
				  	${percent} %
				  </div>
				</div>
				`
			})
			return xhr
		}, 
		success: function (response) {
			console.log("success")
		}, 
		error: function (error) {
			console.log("error")
		}, 
		cache: false, 
		contentType: false, 
		processData: false, 
	})
})