window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('#delete');
  if (el) {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const url = el.getAttribute('data-url');
      fetch(url, { method: 'delete' })
        .then((response) => {
          window.alert('Deleted with sucess')
          window.location.assign('/')
        })
        .catch(() => {
          window.alert('Error! Deletion failed')
        })
    })
  }
})