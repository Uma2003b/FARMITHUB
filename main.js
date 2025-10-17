document.addEventListener('DOMContentLoaded', () => {
  const cropForm = document.getElementById('crop-form');
  const resultContainer = document.getElementById('result-container');
  const recommendedCropSpan = document.getElementById('recommended-crop');
  const paramsSummaryDiv = document.getElementById('params-summary');
  const downloadBtn = document.getElementById('download-btn');

  cropForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(cropForm);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    try {
      const response = await fetch('/crop_recommendation/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const text = await response.text();

      // Parse the returned HTML to extract the recommended crop and params
      const parser = new DOMParser();
      const doc = parser.parseFromString(text, 'text/html');

      const cropElem = doc.querySelector('.crop');
      const paramsElems = doc.querySelectorAll('.param-item');

      if (cropElem) {
        recommendedCropSpan.textContent = cropElem.textContent.replace('🌾 Recommended Crop: ', '').trim();
      } else {
        recommendedCropSpan.textContent = 'No recommendation found';
      }

      // Clear previous summary
      paramsSummaryDiv.innerHTML = '';

      paramsElems.forEach((elem) => {
        paramsSummaryDiv.appendChild(elem.cloneNode(true));
      });

      resultContainer.style.display = 'block';
    } catch (error) {
      alert('Error fetching crop recommendation: ' + error.message);
    }
  });

  downloadBtn.addEventListener('click', () => {
    // Create a form to submit for downloading report
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/crop_recommendation/download_report';

    // Append crop name
    const cropInput = document.createElement('input');
    cropInput.type = 'hidden';
    cropInput.name = 'crop';
    cropInput.value = recommendedCropSpan.textContent;
    form.appendChild(cropInput);

    // Append all input params
    const formData = new FormData(cropForm);
    formData.forEach((value, key) => {
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = key;
      input.value = value;
      form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
  });
});
