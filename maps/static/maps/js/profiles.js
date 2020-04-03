let
  warningCancel = document.getElementById('warning-cancel'),
  warningCancelWarning = document.getElementById('warning-cancel-warning');

warningCancel.addEventListener('click', function () {
  console.info('clicked');
  if (warningCancelWarning.visibility = 'collapse') {
    warningCancelWarning.visibility = 'visible'
    console.log('v');
  } else {
    warningCancelWarning.visibility = 'collapse';
    console.log('c');
  }
});
