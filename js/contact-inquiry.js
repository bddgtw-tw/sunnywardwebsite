(function () {
  const form = document.getElementById('contact-inquiry-form');
  const panel = document.getElementById('inquiry-actions');
  const emailLink = document.getElementById('inquiry-email-action');
  const whatsappLink = document.getElementById('inquiry-whatsapp-action');
  const copyButton = document.getElementById('inquiry-copy-action');
  const status = document.getElementById('inquiry-status');
  if (!form || !panel || !emailLink || !whatsappLink || !copyButton || !status) return;

  const lang = document.documentElement.lang;
  const text = lang === 'zh-TW' ? {
    prefix: 'Sunnyward 專案詢價：', ready: '詢價草稿已準備完成，但尚未送出。請選擇 Email 或 WhatsApp，並在開啟的應用程式中確認送出。', copied: '詢價草稿已複製。', copyFail: '無法自動複製，請改用 Email 或 WhatsApp。',
    labels: { name: '姓名', company: '公司／組織', email: '電子信箱', phone: '電話', projectType: '專案類型', market: '交貨城市／國家', quantity: '預估數量', timeline: '目標交貨時程', subject: '主旨', message: '需求內容', source: '來源頁面' }
  } : lang === 'ja' ? {
    prefix: 'Sunnyward プロジェクトお問い合わせ：', ready: 'お問い合わせ下書きを作成しました。まだ送信されていません。Email または WhatsApp を選び、開いたアプリで送信を確定してください。', copied: 'お問い合わせ下書きをコピーしました。', copyFail: '自動コピーできませんでした。Email または WhatsApp をご利用ください。',
    labels: { name: 'お名前', company: '会社・組織名', email: 'メール', phone: '電話', projectType: 'プロジェクト種別', market: '納品先の都市／国', quantity: '予定数量', timeline: '希望納期', subject: '件名', message: 'お問い合わせ内容', source: '参照ページ' }
  } : {
    prefix: 'Sunnyward project enquiry: ', ready: 'Your enquiry draft is ready, but it has not been sent. Choose Email or WhatsApp and confirm sending in the app that opens.', copied: 'Enquiry draft copied.', copyFail: 'Automatic copying was unavailable. Please use Email or WhatsApp.',
    labels: { name: 'Name', company: 'Company / organisation', email: 'Email', phone: 'Phone', projectType: 'Project type', market: 'Delivery city / country', quantity: 'Estimated quantity', timeline: 'Target delivery timing', subject: 'Subject', message: 'Requirements', source: 'Source page' }
  };

  function value(name) {
    return (new FormData(form).get(name) || '').toString().trim();
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const subject = value('subject');
    const lines = [
      `${text.labels.name}: ${value('name')}`,
      value('company') ? `${text.labels.company}: ${value('company')}` : '',
      `${text.labels.email}: ${value('email')}`,
      value('phone') ? `${text.labels.phone}: ${value('phone')}` : '',
      '', `${text.labels.message}:`, value('message'),
      '', `${text.labels.source}: ${window.location.href}`
    ].filter((line, index, lines) => line !== '' || (index > 0 && lines[index - 1] !== ''));
    const draft = lines.join('\n');
    emailLink.href = `mailto:sales@sunnyward.com?subject=${encodeURIComponent(text.prefix + subject)}&body=${encodeURIComponent(draft)}`;
    const waBase = Math.random() < 0.5 ? 'https://wa.me/60165262894' : 'https://wa.me/60167252894';
    whatsappLink.href = `${waBase}?text=${encodeURIComponent(text.prefix + subject + '\n\n' + draft)}`;
    copyButton.dataset.draft = draft;
    status.textContent = text.ready;
    panel.hidden = false;
    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });

  copyButton.addEventListener('click', async function () {
    const draft = copyButton.dataset.draft || '';
    try {
      await navigator.clipboard.writeText(draft);
      status.textContent = text.copied;
    } catch (error) {
      status.textContent = text.copyFail;
    }
  });
})();
