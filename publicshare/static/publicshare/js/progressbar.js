
const fileinput = document.getElementById('fileuploadForm')
const filetitle = document.getElementById('titleForm')
const uploadBtn = document.getElementById('upload-btn')
const progressBox = document.getElementById('progress-box')
const csrftoken = document.getElementsByName('csrfmiddlewaretoken')

uploadBtn.addEventListener('click', () => {
	progressBox.style = "display:_;"
	uploadBtn.style = "display:none;"

	const fd = new FormData()
	fd.append('csrfmiddlewaretoken', csrftoken[0].value)
	fd.append('file', fileinput.files[0])
	fd.append('title', filetitle.value)

	let percent = 0.0;

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
				percent = ( 100 * e.loaded / e.total ).toFixed( 1 )
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
		success: function (jsonResponse) {
			window.location.href = jsonResponse.href
	    }, 
		error: function (error) {
			console.log("error at percent " + percent)
			progressBox.innerHTML = `
			<div class="progress">
			  <div class="progress-bar bg-danger" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100">
			  	Something went wrong...
			  </div>
			</div><br>
			<a href="/public/" type="button" class="btn btn-outline-danger btn-lg" style="width:80%;">돌아가기</a>
			`
		}, 
		cache: false, 
		contentType: false, 
		processData: false, 
	})
})