const accessToken = '3796899bd37c423bad3a21a25277bce0';
const baseUrl = 'https://api.api.ai/api/query?v=2015091001';
const sessionId = '20150910';
const loader = `<span class='loader'><span class='loader__dot'></span><span class='loader__dot'></span><span class='loader__dot'></span></span>`;
const errorMessage = 'My apologies, I\'m not avail at the moment, however, feel free to call our support team directly 0123456789.';
const urlPattern = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
const $document = document;
const $chatbot = $document.querySelector('.chatbot');
const $chatbotMessageWindow = $document.querySelector('.chatbot__message-window');
const $chatbotHeader = $document.querySelector('.chatbot__header');
const $chatbotMessages = $document.querySelector('.chatbot__messages');
const $chatbotInput = $document.querySelector('.chatbot__input');
const $chatbotSubmit = $document.querySelector('.chatbot__submit');

const botLoadingDelay = 1000;
const botReplyDelay = 2000;

document.addEventListener('keypress', event => {
  if (event.which == 13) validateMessage();
}, false);

$chatbotHeader.addEventListener('click', () => {
  console.log("Se preciono click");
  toggle($chatbot, 'chatbot--closed');
  $chatbotInput.focus();
}, false);

$chatbotSubmit.addEventListener('click', () => {
  validateMessage();
}, false);

const toggle = (element, klass) => {
    const classes = element.className.match(/\S+/g) || [],
    index = classes.indexOf(klass);
    index >= 0 ? classes.splice(index, 1) : classes.push(klass);
    element.className = classes.join(' ');
  };