const state = {
  panchanga: null,
  cosmic: null,
  selectedPlanet: null,
  location: { latitude: 25.3176, longitude: 82.9739, elevation: 0, timezone: 'Asia/Kolkata' },
  calendarMonth: null,
  festivalMonths: new Map(),
  language: 'en',
};
const icons = ['☾', '✦', '◉', '♆'];
const $ = (selector) => document.querySelector(selector);
const translations = {
  en: { today: 'Today', liveClock: 'Live Clock', todaysPanchanga: 'Today’s Panchanga', festivalCalendar: 'Festival Calendar', location: 'Location', cosmos: 'Cosmos', cosmicPanchanga: 'COSMIC PANCHANGA · LAHIRI AYANAMSHA', skyBehind: 'The sky behind today’s Panchanga', loadingSidereal: 'Loading sidereal positions', celestialPlayback: 'CELESTIAL PLAYBACK', scrubSky: 'Scrub through the sky from seven days ago to thirty days ahead.', siderealSky: 'SIDEREAL SKY', planetaryLongitudes: 'Planetary longitudes', live: '● LIVE', rashi30: 'Rashi 30°', moonPath: 'Moon path', planet: 'Planet', whyToday: 'WHY TODAY', fourValues: 'Four values, one moving sky', calculationLocation: 'Calculation Location', selectedLocation: 'Selected location', calculating: 'Calculating', liveCalculation: 'Live calculation', localTimeWindows: 'Local time windows', sunrise: 'Sunrise', sunset: 'Sunset', moonrise: 'Moonrise', moonset: 'Moonset', now: 'Now', brahmaMuhurta: 'Brahma Muhurta', rahuKaal: 'Rahu Kaal', unavailable: 'Unavailable', tithi: 'Tithi', nakshatra: 'Nakshatra', yoga: 'Yoga', karana: 'Karana', calculatedLocally: 'Calculated locally', comingFestivals: 'Coming Festivals', calendar: 'Calendar', solarLunar: 'Solar / Lunar Telemetry', changeLocation: 'Change location', recalculate: 'Recalculate', todayButton: 'Today', eventsIn: 'Events in', noEvents: 'No catalog events for this month.', panchangaFor: 'Panchanga for', calculationDetails: 'Calculation details', localPanchanga: 'GHADI / LOCAL PANCHANGA', comingCelebrations: 'COMING CELEBRATIONS', solarDailyWindows: 'Solar, lunar, and daily time windows', liveDetails: 'LIVE DETAILS', viewDetails: 'View details', noUpcoming: 'No catalog events in the next three months.', calculatedFor: 'Calculated for', calculatingLocation: 'Calculating Panchanga data for the selected location.', enterLocation: 'Enter a location and recalculate.', locationLinkNote: 'This link carries the location; nothing is stored on the server.', liveLocalTime: 'LIVE LOCAL TIME', calculateForLocation: 'Calculate for any location', locationCalibration: 'LOCATION CALIBRATION', latitude: 'Latitude', longitude: 'Longitude', timezoneLabel: 'Timezone', elevation: 'Elevation (metres)', useDeviceLocation: 'Use device location', copyShareLink: 'Copy share link', calendarNote: 'Lunar observance dates can vary by region and tradition. This catalog is a maintained pan-Indian reference.', panIndianObservances: 'PAN-INDIAN OBSERVANCES', language: 'Language', mainNavigation: 'Main navigation', weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] },
  siderealExplain: 'Sidereal longitudes explain the Panchanga values below.',
  direct: 'Direct',
  retrograde: 'Retrograde',
  nextTithi: 'Next Tithi',
  tithiBoundary: 'Tithi boundary',
  moonEnters: 'Moon enters',
  laterToday: 'later today',
  hi: { today: 'आज', liveClock: 'सजीव समय', todaysPanchanga: 'आज का पंचांग', festivalCalendar: 'पर्व कैलेंडर', location: 'स्थान', cosmos: 'ब्रह्मांड', cosmicPanchanga: 'ब्रह्मांडीय पंचांग · लाहिड़ी अयनांश', skyBehind: 'आज के पंचांग के पीछे का आकाश', loadingSidereal: 'निरयन स्थितियां लोड हो रही हैं', celestialPlayback: 'आकाशीय समय यात्रा', scrubSky: 'सात दिन पीछे से तीस दिन आगे तक आकाश की गति देखें।', siderealSky: 'निरयन आकाश', planetaryLongitudes: 'ग्रहों की देशांतर स्थिति', live: '● लाइव', rashi30: 'राशि 30°', moonPath: 'चंद्र पथ', planet: 'ग्रह', whyToday: 'आज ऐसा क्यों', fourValues: 'चार मान, एक गतिमान आकाश', calculationLocation: 'गणना स्थान', selectedLocation: 'चयनित स्थान', calculating: 'गणना हो रही है', liveCalculation: 'सजीव गणना', localTimeWindows: 'स्थानीय समय अवधि', sunrise: 'सूर्योदय', sunset: 'सूर्यास्त', moonrise: 'चंद्रोदय', moonset: 'चंद्रास्त', now: 'अभी', brahmaMuhurta: 'ब्रह्म मुहूर्त', rahuKaal: 'राहु काल', unavailable: 'उपलब्ध नहीं', tithi: 'तिथि', nakshatra: 'नक्षत्र', yoga: 'योग', karana: 'करण', calculatedLocally: 'स्थान के अनुसार गणना', comingFestivals: 'आगामी पर्व', calendar: 'कैलेंडर', solarLunar: 'सौर / चंद्र विवरण', changeLocation: 'स्थान बदलें', recalculate: 'पुनः गणना', todayButton: 'आज', eventsIn: 'इस महीने के पर्व', noEvents: 'इस महीने कोई पर्व नहीं है।', panchangaFor: 'का पंचांग', calculationDetails: 'गणना विवरण', localPanchanga: 'आयनम / स्थानीय पंचांग', comingCelebrations: 'आगामी उत्सव', solarDailyWindows: 'सौर, चंद्र और दैनिक समय अवधि', liveDetails: 'सजीव विवरण', viewDetails: 'विवरण देखें', noUpcoming: 'अगले तीन महीनों में कोई पर्व सूचीबद्ध नहीं है।', calculatedFor: 'की गणना', calculatingLocation: 'चयनित स्थान के लिए पंचांग की गणना हो रही है।', enterLocation: 'स्थान दर्ज करके फिर से गणना करें।', locationLinkNote: 'स्थान इस लिंक में है; सर्वर पर सहेजा नहीं जाता।', liveLocalTime: 'स्थानीय समय', calculateForLocation: 'किसी भी स्थान के लिए गणना', locationCalibration: 'स्थान निर्धारण', latitude: 'अक्षांश', longitude: 'देशांतर', timezoneLabel: 'समय क्षेत्र', elevation: 'ऊंचाई (मीटर)', useDeviceLocation: 'डिवाइस का स्थान लें', copyShareLink: 'साझा लिंक कॉपी करें', calendarNote: 'चंद्र पर्वों की तिथियां क्षेत्र और परंपरा के अनुसार बदल सकती हैं। यह अखिल भारतीय संदर्भ सूची है।', panIndianObservances: 'अखिल भारतीय पर्व', language: 'भाषा', mainNavigation: 'मुख्य नेविगेशन', weekdays: ['रवि', 'सोम', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि'] },
};
const cosmicTranslations = {
  en: {
    siderealExplain: 'Sidereal longitudes explain the Panchanga values below.', direct: 'Direct', retrograde: 'Retrograde', nextTithi: 'Next Tithi', tithiBoundary: 'Tithi boundary', moonEnters: 'Moon enters', laterToday: 'later today', moonSun: 'Moon − Sun', eachSpan: 'Each span = 13°20′', sunMoonNormalized: 'Sun + Moon, normalized to 360°', angleSpan: 'Angle / 13°20′', tithiHalves: 'Tithi is divided into two halves', elongationHalf: 'Elongation / 6°', sidereal: 'sidereal', perDay: '°/day', planetaryTelemetry: 'PLANETARY TELEMETRY', positionsSelected: 'Positions at the selected time', upNext: 'UP NEXT', transitionsHorizon: 'Transitions on the horizon', calculatedVelocity: 'Calculated from current velocity', educationalView: 'EDUCATIONAL VIEW', solarContext: 'Solar system context', showOrbitModel: 'Show orbit model', hideOrbitModel: 'Hide orbit model', longitudeLabel: 'Longitude', rashiLabel: 'Rashi', nakshatraLabel: 'Nakshatra', padaLabel: 'Pada', motionLabel: 'Motion', speedLabel: 'Speed',
  },
  hi: {
    siderealExplain: 'निरयन देशांतर नीचे दिए गए पंचांग मानों को समझाते हैं।', direct: 'मार्गी', retrograde: 'वक्री', nextTithi: 'अगली तिथि', tithiBoundary: 'तिथि सीमा', moonEnters: 'चंद्रमा का प्रवेश', laterToday: 'आज बाद में', moonSun: 'चंद्र − सूर्य', eachSpan: 'प्रत्येक विस्तार = 13°20′', sunMoonNormalized: 'सूर्य + चंद्र, 360° में सामान्यीकृत', angleSpan: 'कोण / 13°20′', tithiHalves: 'तिथि को दो करणों में बांटा जाता है', elongationHalf: 'देशांतर अंतर / 6°', sidereal: 'निरयन', perDay: '°/दिन', planetaryTelemetry: 'ग्रह स्थिति विवरण', positionsSelected: 'चयनित समय पर ग्रहों की स्थिति', upNext: 'आगे आने वाले परिवर्तन', transitionsHorizon: 'क्षितिज पर आने वाले परिवर्तन', calculatedVelocity: 'वर्तमान गति से गणना', educationalView: 'शैक्षिक दृश्य', solarContext: 'सौर मंडल का संदर्भ', showOrbitModel: 'कक्षा मॉडल दिखाएं', hideOrbitModel: 'कक्षा मॉडल छिपाएं', longitudeLabel: 'देशांतर', rashiLabel: 'राशि', nakshatraLabel: 'नक्षत्र', padaLabel: 'पद', motionLabel: 'गति', speedLabel: 'वेग',
  },
};
const hindiTerms = {
  Pratipada: 'प्रतिपदा', Dwitiya: 'द्वितीया', Tritiya: 'तृतीया', Chaturthi: 'चतुर्थी', Panchami: 'पंचमी',
  Shashthi: 'षष्ठी', Saptami: 'सप्तमी', Ashtami: 'अष्टमी', Navami: 'नवमी', Dashami: 'दशमी',
  Ekadashi: 'एकादशी', Dwadashi: 'द्वादशी', Trayodashi: 'त्रयोदशी', Chaturdashi: 'चतुर्दशी',
  Purnima: 'पूर्णिमा', Amavasya: 'अमावस्या',
  Aries: 'मेष', Taurus: 'वृषभ', Gemini: 'मिथुन', Cancer: 'कर्क', Leo: 'सिंह', Virgo: 'कन्या', Libra: 'तुला', Scorpio: 'वृश्चिक', Sagittarius: 'धनु', Capricorn: 'मकर', Aquarius: 'कुंभ', Pisces: 'मीन',
  Sun: 'सूर्य', Moon: 'चंद्र', Mars: 'मंगल', Mercury: 'बुध', Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु',
  Ashwini: 'अश्विनी', Bharani: 'भरणी', Krittika: 'कृत्तिका', Rohini: 'रोहिणी', Mrigashira: 'मृगशीर्ष',
  Ardra: 'आर्द्रा', Punarvasu: 'पुनर्वसु', Pushya: 'पुष्य', Ashlesha: 'आश्लेषा', Magha: 'मघा',
  'Purva Phalguni': 'पूर्व फाल्गुनी', 'Uttara Phalguni': 'उत्तर फाल्गुनी', Hasta: 'हस्त', Chitra: 'चित्रा',
  Swati: 'स्वाती', Vishakha: 'विशाखा', Anuradha: 'अनुराधा', Jyeshtha: 'ज्येष्ठा', Mula: 'मूल',
  'Purva Ashadha': 'पूर्वाषाढ़ा', 'Uttara Ashadha': 'उत्तराषाढ़ा', Shravana: 'श्रवण', Dhanishta: 'धनिष्ठा',
  Shatabhisha: 'शतभिषा', 'Purva Bhadrapada': 'पूर्व भाद्रपद', 'Uttara Bhadrapada': 'उत्तर भाद्रपद', Revati: 'रेवती',
  Vishkambha: 'विष्कम्भ', Priti: 'प्रीति', Ayushman: 'आयुष्मान', Saubhagya: 'सौभाग्य', Shobhana: 'शोभन',
  Atiganda: 'अतिगण्ड', Sukarma: 'सुकर्मा', Dhriti: 'धृति', Shula: 'शूल', Ganda: 'गण्ड', Vriddhi: 'वृद्धि',
  Dhruva: 'ध्रुव', Vyaghata: 'व्याघात', Harshana: 'हर्षण', Vajra: 'वज्र', Siddhi: 'सिद्धि',
  Vyatipata: 'व्यतीपात', Variyana: 'वरीयान', Parigha: 'परिघ', Shiva: 'शिव', Siddha: 'सिद्ध',
  Sadhya: 'साध्य', Shubha: 'शुभ', Shukla: 'शुक्ल', Brahma: 'ब्रह्म', Indra: 'इन्द्र', Vaidhriti: 'वैधृति',
  Kimstughna: 'किंस्तुघ्न', Bava: 'बव', Balava: 'बालव', Kaulava: 'कौलव', Taitila: 'तैतिल', Gara: 'गर',
  Vanija: 'वणिज', Vishti: 'विष्टि', Shakuni: 'शकुनि', Chatushpada: 'चतुष्पद', Naga: 'नाग',
  'Sun enters Capricorn': 'सूर्य का मकर राशि में प्रवेश', 'National observance': 'राष्ट्रीय पर्व',
  'Spring festival honoring Saraswati': 'वसंत ऋतु का सरस्वती पूजा उत्सव', 'Murugan observance': 'भगवान मुरुगन का पर्व',
  'Festival of colors': 'रंगों का उत्सव', 'Birth of Lord Rama': 'भगवान राम का जन्मोत्सव',
  'Harvest and Sikh new year observance': 'फसल पर्व और सिख नववर्ष',
  'Birth, enlightenment, and parinirvana of Buddha': 'बुद्ध का जन्म, ज्ञान प्राप्ति और महापरिनिर्वाण',
  'Jagannath chariot festival': 'जगन्नाथ रथ यात्रा', 'Honoring teachers and gurus': 'गुरुजनों और आचार्यों का सम्मान',
  'Celebration between siblings': 'भाई-बहन के स्नेह का उत्सव', 'Kerala harvest festival': 'केरल का फसल उत्सव',
  'Birth of Lord Ganesha': 'भगवान गणेश का जन्मोत्सव', 'Nine nights of divine worship': 'देवी आराधना की नौ रातें',
  'Victory of good over evil': 'बुराई पर अच्छाई की विजय', 'Festival of lights': 'दीपों का उत्सव',
  'Birth of Guru Nanak Dev Ji': 'गुरु नानक देव जी का प्रकाश पर्व', 'Christian observance': 'ईसाई पर्व',
  'Night of Lord Shiva': 'भगवान शिव की आराधना की रात्रि', 'Birth of Lord Krishna': 'भगवान कृष्ण का जन्मोत्सव',
  'Navratri begins': 'नवरात्रि प्रारंभ', 'Gandhi Jayanti': 'गांधी जयंती', Dussehra: 'दशहरा', Onam: 'ओणम', 'Ganesh Chaturthi': 'गणेश चतुर्थी',
  'Makar Sankranti': 'मकर संक्रांति', Holi: 'होली', Diwali: 'दीपावली', 'Maha Shivaratri': 'महाशिवरात्रि', Janmashtami: 'जन्माष्टमी',
};

function t(key) {
  return translations[state.language][key] || translations.en[key] || cosmicTranslations[state.language]?.[key] || cosmicTranslations.en?.[key] || translations[key] || key;
}

function localizedTerm(value) {
  return state.language === 'hi' ? hindiTerms[value] || value : value;
}

function calculationDateLine(date, timezone) {
  return state.language === 'hi'
    ? `दिनांक ${formatDate(date)} · समय क्षेत्र ${timezone}`
    : `${t('calculatedFor')} ${formatDate(date)} in ${timezone}`;
}

function calculationLocationLine(date, latitude, longitude, timezone) {
  return state.language === 'hi'
    ? `${formatDate(date)} की गणना · ${Math.abs(latitude).toFixed(4)}° ${latitude < 0 ? 'दक्षिण' : 'उत्तर'}, ${Math.abs(longitude).toFixed(4)}° ${longitude < 0 ? 'पश्चिम' : 'पूर्व'} · ${timezone}`
    : `${t('calculatedFor')} ${formatDate(date)} using ${latitude.toFixed(4)}°, ${longitude.toFixed(4)}°, and ${timezone}.`;
}

function wallParts(value) {
  if (!value) return null;
  const match = String(value).match(/(\d{4})-(\d{2})-(\d{2})T?(\d{2})?:(\d{2})?/);
  if (!match) return null;
  return { year: Number(match[1]), month: Number(match[2]), day: Number(match[3]), hour: Number(match[4] || 0), minute: Number(match[5] || 0) };
}

function formatTime(value) {
  const parts = wallParts(value);
  if (!parts) return 'Unavailable';
  return new Intl.DateTimeFormat(state.language === 'hi' ? 'hi-IN' : undefined, { hour: 'numeric', minute: '2-digit', hour12: true, timeZone: 'UTC' })
    .format(new Date(Date.UTC(2000, 0, 1, parts.hour, parts.minute)));
}

function formatDate(value) {
  const parts = wallParts(value);
  if (!parts) return 'Unavailable';
  return new Intl.DateTimeFormat(state.language === 'hi' ? 'hi-IN' : undefined, { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })
    .format(new Date(Date.UTC(parts.year, parts.month - 1, parts.day, 12)));
}

function minutesSinceMidnight(value) {
  const parts = wallParts(value);
  return parts ? parts.hour * 60 + parts.minute : null;
}

function setClock() {
  const formatter = new Intl.DateTimeFormat(state.language === 'hi' ? 'hi-IN' : undefined, {
    hour: 'numeric', minute: '2-digit', second: '2-digit', hour12: true, timeZone: state.location.timezone,
  });
  const currentTime = formatter.format(new Date());
  $('#hero-time').textContent = currentTime;
  $('#hero-period').textContent = state.location.timezone;
  $('#large-time').textContent = currentTime;
  $('#clock-zone').textContent = state.location.timezone;
  $('#now-marker span').textContent = t('now');
  const parts = Object.fromEntries(formatter.formatToParts(new Date()).filter((part) => part.type !== 'literal').map((part) => [part.type, part.value]));
  const hour = Number(parts.hour) % 12;
  const minute = Number(parts.minute);
  $('#clock-hour-hand').style.transform = `rotate(${hour * 30 + minute * 0.5}deg)`;
  $('#clock-minute-hand').style.transform = `rotate(${minute * 6}deg)`;
  setTimelinePosition('#now-marker', Number(parts.hour) * 60 + Number(parts.minute));
}

function setTimelinePosition(selector, minutes) {
  const element = $(selector);
  if (!Number.isFinite(minutes)) {
    element.hidden = true;
    return;
  }
  element.hidden = false;
  element.style.setProperty('--position', `${(minutes / 1440) * 100}%`);
}

function setCelestialMarker(selector, label, value) {
  const minutes = minutesSinceMidnight(value);
  const element = $(selector);
  setTimelinePosition(selector, minutes);
  const translatedLabel = t(label);
  element.querySelector('b').textContent = minutes === null ? `${translatedLabel} ${t('unavailable')}` : `${translatedLabel} ${formatTime(value)}`;
}

function setDaylight(sunriseValue, sunsetValue) {
  const sunrise = minutesSinceMidnight(sunriseValue);
  const sunset = minutesSinceMidnight(sunsetValue);
  const element = $('#daylight-window');
  if (sunrise === null || sunset === null || sunset <= sunrise) {
    element.hidden = true;
    return;
  }
  element.hidden = false;
  element.style.setProperty('--start', `${(sunrise / 1440) * 100}%`);
  element.style.setProperty('--span', `${((sunset - sunrise) / 1440) * 100}%`);
}

function setWindow(selector, label, startValue, endValue) {
  const start = minutesSinceMidnight(startValue);
  const end = minutesSinceMidnight(endValue);
  const element = $(selector);
  if (start === null) {
    element.textContent = t('unavailable');
    element.style.removeProperty('--start');
    element.style.removeProperty('--span');
    return;
  }
  const span = end === null ? 30 : Math.max(20, (end >= start ? end : end + 1440) - start);
  element.textContent = `${t(label)} · ${formatTime(startValue)}${endValue ? ` – ${formatTime(endValue)}` : ''}`;
  element.style.setProperty('--start', `${(start / 1440) * 100}%`);
  element.style.setProperty('--span', `${Math.min(100 - (start / 1440) * 100, (span / 1440) * 100)}%`);
}

function renderFacts(lunar) {
  return [
    ['tithi', lunar.tithi_name], ['nakshatra', lunar.nakshatra_name],
    ['yoga', lunar.yoga_name], ['karana', lunar.karana_name],
  ].map(([label, value], index) => `<article class="fact"><span class="symbol">${icons[index]}</span><p>${t(label)}</p><h3>${localizedTerm(value) || t('unavailable')}</h3><p>${t('calculatedLocally')}</p><span class="meter"></span></article>`).join('');
}

function monthKey(year, month) {
  return `${year}-${String(month).padStart(2, '0')}`;
}

function calendarDate(value) {
  const parts = wallParts(value);
  return parts ? `${parts.year}-${String(parts.month).padStart(2, '0')}-${String(parts.day).padStart(2, '0')}` : '';
}

function monthLabel(year, month) {
  return new Intl.DateTimeFormat(state.language === 'hi' ? 'hi-IN' : undefined, { month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date(Date.UTC(year, month - 1, 1)));
}

function renderFestivals() {
  const month = state.calendarMonth;
  const events = month ? state.festivalMonths.get(monthKey(month.year, month.month))?.festivals || [] : [];
  $('#calendar-count').textContent = `${events.length} observance${events.length === 1 ? '' : 's'}`;
  $('#calendar-events-count').textContent = events.length;
  const currentDate = calendarDate(state.panchanga?.date);
  const upcoming = [...state.festivalMonths.values()].flatMap((calendar) => calendar.festivals)
    .filter((festival) => calendarDate(festival.date) >= currentDate).sort((first, second) => first.date.localeCompare(second.date)).slice(0, 3);
  $('#upcoming-list').innerHTML = upcoming.length
    ? upcoming.map((festival) => `<article class="upcoming-item"><h3>${localizedTerm(festival.name)}</h3><time datetime="${calendarDate(festival.date)}">${formatDate(festival.date)}</time></article>`).join('')
    : `<p class="empty-copy">${t('noUpcoming')}</p>`;
  $('#calendar-title').textContent = month ? monthLabel(month.year, month.month) : t('festivalCalendar');
  $('#calendar-events-title').textContent = month ? `${t('eventsIn')} ${monthLabel(month.year, month.month)}` : t('eventsIn');
  $('#calendar-events-list').innerHTML = events.length
    ? events.map((festival) => `<article class="calendar-event"><small>${formatDate(festival.date)}</small><strong>${localizedTerm(festival.name)}</strong><p>${localizedTerm(festival.significance) || ''}</p></article>`).join('')
    : `<p class="empty-copy">${t('noEvents')}</p>`;
  if (!month) return;
  const firstWeekday = new Date(Date.UTC(month.year, month.month - 1, 1)).getUTCDay();
  const daysInMonth = new Date(Date.UTC(month.year, month.month, 0)).getUTCDate();
  const eventsByDay = events.reduce((days, festival) => {
    const day = wallParts(festival.date).day;
    days.set(day, [...(days.get(day) || []), festival]);
    return days;
  }, new Map());
  const cells = Array.from({ length: firstWeekday }, () => '<div class="calendar-day muted-day"></div>');
  for (let day = 1; day <= daysInMonth; day += 1) {
    const festivals = eventsByDay.get(day) || [];
    const isToday = calendarDate(state.panchanga?.date) === `${month.year}-${String(month.month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    cells.push(`<article class="calendar-day${festivals.length ? ' has-festival' : ''}${isToday ? ' today' : ''}"><span>${day}</span>${festivals.map((festival) => `<strong class="festival-chip ${festival.significance === 'National observance' ? 'national-chip' : 'lunar-chip'}" title="${localizedTerm(festival.name)}">${localizedTerm(festival.name)}</strong>`).join('')}</article>`);
  }
  $('#calendar-grid').innerHTML = cells.join('');
}

async function loadFestivalMonths(anchorDate) {
  const parts = wallParts(anchorDate);
  if (!parts) return;
  const requests = Array.from({ length: 4 }, (_, offset) => {
    const date = new Date(Date.UTC(parts.year, parts.month - 1 + offset, 1));
    const year = date.getUTCFullYear();
    const month = date.getUTCMonth() + 1;
    return request(`/festival/calendar?year=${year}&month=${month}`).then((calendar) => {
      state.festivalMonths.set(monthKey(year, month), calendar);
      return calendar;
    });
  });
  await Promise.all(requests);
  state.calendarMonth = { year: parts.year, month: parts.month };
  renderFestivals();
}

async function changeCalendarMonth(offset) {
  if (!state.calendarMonth) return;
  const date = new Date(Date.UTC(state.calendarMonth.year, state.calendarMonth.month - 1 + offset, 1));
  const year = date.getUTCFullYear();
  const month = date.getUTCMonth() + 1;
  const key = monthKey(year, month);
  if (!state.festivalMonths.has(key)) state.festivalMonths.set(key, await request(`/festival/calendar?year=${year}&month=${month}`));
  state.calendarMonth = { year, month };
  renderFestivals();
}

function render() {
  const panchanga = state.panchanga;
  const lunar = panchanga?.lunar || {};
  const solar = panchanga?.solar || {};
  const windows = panchanga?.time_windows || {};
  setWindow('#brahma-window', 'brahmaMuhurta', windows.brahma_muhurta_start, null);
  setWindow('#rahu-window', 'rahuKaal', windows.rahu_kaal_start, windows.rahu_kaal_end);
  setDaylight(solar.sunrise, solar.sunset);
  setCelestialMarker('#sunrise-marker', 'sunrise', solar.sunrise);
  setCelestialMarker('#sunset-marker', 'sunset', solar.sunset);
  setCelestialMarker('#moonrise-marker', 'moonrise', solar.moonrise);
  setCelestialMarker('#moonset-marker', 'moonset', solar.moonset);
  $('#fact-grid').innerHTML = renderFacts(lunar);
  $('#day-sunrise').textContent = formatTime(solar.sunrise);
  $('#day-sunset').textContent = formatTime(solar.sunset);
  $('#day-moonrise').textContent = formatTime(solar.moonrise);
  $('#day-moonset').textContent = formatTime(solar.moonset);
  $('#day-brahma').textContent = formatTime(windows.brahma_muhurta_start);
  $('#day-rahu').textContent = windows.rahu_kaal_start ? `${formatTime(windows.rahu_kaal_start)} – ${formatTime(windows.rahu_kaal_end)}` : t('unavailable');
  $('#sunrise').textContent = formatTime(solar.sunrise);
  $('#sunset').textContent = formatTime(solar.sunset);
  $('#moonrise').textContent = formatTime(solar.moonrise);
  $('#moonset').textContent = formatTime(solar.moonset);
  $('#sun-cycle').textContent = solar.sunrise ? `${formatTime(solar.sunrise)} ${t('sunrise')} · ${formatTime(solar.sunset)} ${t('sunset')}` : `${t('sunrise')} / ${t('sunset')}`;
  $('#current-heading').textContent = panchanga ? `${localizedTerm(lunar.tithi_name || t('today'))} · ${localizedTerm(lunar.nakshatra_name || t('todaysPanchanga'))}` : t('calculating');
  $('#muhurta-countdown').textContent = panchanga ? calculationDateLine(panchanga.date, state.location.timezone) : t('calculatingLocation');
  $('#hero-summary').textContent = panchanga ? [lunar.tithi_name, lunar.nakshatra_name, lunar.yoga_name, lunar.karana_name].filter(Boolean).map(localizedTerm).join(' | ') : t('calculating');
  $('#guidance-copy').textContent = panchanga
    ? calculationLocationLine(panchanga.date, state.location.latitude, state.location.longitude, state.location.timezone)
    : t('enterLocation');
  $('#clock-detail').textContent = panchanga ? [lunar.tithi_name, lunar.nakshatra_name, lunar.yoga_name].filter(Boolean).map(localizedTerm).join(' · ') : t('calculating');
  $('#panchanga-heading').textContent = panchanga ? `${formatDate(panchanga.date)} ${t('panchangaFor')}` : t('todaysPanchanga');
  $('#detail-grid').innerHTML = [
    ['tithi', [lunar.tithi_name, lunar.paksha].filter(Boolean).map(localizedTerm).join(' ')], ['nakshatra', localizedTerm(lunar.nakshatra_name)],
    ['yoga', localizedTerm(lunar.yoga_name)], ['karana', localizedTerm(lunar.karana_name)], ['sunrise', formatTime(solar.sunrise)],
    ['sunset', formatTime(solar.sunset)], ['moonrise', formatTime(solar.moonrise)], ['moonset', formatTime(solar.moonset)],
    ['rahuKaal', windows.rahu_kaal_start ? `${formatTime(windows.rahu_kaal_start)} – ${formatTime(windows.rahu_kaal_end)}` : t('unavailable')],
  ].map(([label, value]) => `<article class="detail"><small>${t(label)}</small><strong>${value || t('unavailable')}</strong></article>`).join('');
  renderFestivals();
  setClock();
  renderCosmos();
}

const rashiNames = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
const nakshatraNames = ['Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'];

function polarPoint(cx, cy, radius, degrees) {
  const angle = (degrees - 90) * Math.PI / 180;
  return [cx + radius * Math.cos(angle), cy + radius * Math.sin(angle)];
}

function renderCosmos() {
  const cosmic = state.cosmic;
  if (!cosmic) return;
  $('#cosmos-date').textContent = `${formatDate(state.panchanga?.date)} · ${state.location.timezone}`;
  $('#cosmos-time').textContent = t('siderealExplain');
  $('#cosmos-sun').textContent = `${cosmic.sun_longitude.toFixed(2)}°`;
  $('#cosmos-moon').textContent = `${cosmic.moon_longitude.toFixed(2)}°`;
  $('#cosmos-ayanamsha').textContent = `${cosmic.ayanamsha} · ${cosmic.ayanamsha_degrees}°`;

  const wheel = $('#zodiac-wheel');
  const cx = 260; const cy = 260;
  const svg = [`<circle class="wheel-bg" cx="${cx}" cy="${cy}" r="238"/>`, `<circle class="wheel-ring" cx="${cx}" cy="${cy}" r="205"/>`, `<circle class="nakshatra-ring" cx="${cx}" cy="${cy}" r="226"/>`];
  rashiNames.forEach((name, index) => {
    const start = index * 30;
    const [x1, y1] = polarPoint(cx, cy, 205, start);
    const [x2, y2] = polarPoint(cx, cy, 205, start + 30);
    const [labelX, labelY] = polarPoint(cx, cy, 180, start + 15);
    svg.push(`<path class="wheel-spoke" d="M ${cx} ${cy} L ${x1} ${y1}"/><path class="wheel-spoke" d="M ${cx} ${cy} L ${x2} ${y2}"/><text class="rashi-label" x="${labelX}" y="${labelY}">${name}</text>`);
  });
  nakshatraNames.forEach((name, index) => {
    const angle = index * (360 / 27) + 360 / 54;
    const [x, y] = polarPoint(cx, cy, 226, angle);
    svg.push(`<text class="nakshatra-label" x="${x}" y="${y}" transform="rotate(${angle} ${x} ${y})">${name}</text>`);
  });
  cosmic.planets.forEach((planet) => {
    const [x, y] = polarPoint(cx, cy, planet.name === 'Moon' ? 150 : 166, planet.longitude);
    svg.push(`<g class="planet-mark" data-planet="${planet.name}" tabindex="0"><circle cx="${x}" cy="${y}" r="${planet.name === 'Moon' ? 9 : 7}"/><text x="${x}" y="${y + 4}">${planet.symbol}</text></g>`);
  });
  svg.push(`<circle class="wheel-core" cx="${cx}" cy="${cy}" r="32"/><text class="wheel-core-label" x="${cx}" y="${cy + 4}">SIDEREAL</text>`);
  wheel.innerHTML = svg.join('');
  wheel.querySelectorAll('.planet-mark').forEach((mark) => {
    const planet = cosmic.planets.find((item) => item.name === mark.dataset.planet);
    mark.addEventListener('mouseenter', () => showPlanetTooltip(planet, mark));
    mark.addEventListener('focus', () => showPlanetTooltip(planet, mark));
    mark.addEventListener('click', () => openPlanetDrawer(planet, mark));
    mark.addEventListener('mouseleave', () => { $('#planet-tooltip').hidden = true; });
    mark.addEventListener('blur', () => { $('#planet-tooltip').hidden = true; });
  });
  $('#cosmic-facts').innerHTML = [
    [t('tithi'), `${t('moonSun')} = ${cosmic.elongation.toFixed(1)}°`, `${cosmic.elongation.toFixed(1)}° / 12° = ${(cosmic.elongation / 12).toFixed(2)}`, `${localizedTerm(cosmic.paksha)} ${localizedTerm(cosmic.tithi_name)}`],
    [t('nakshatra'), `Moon = ${cosmic.moon_longitude.toFixed(1)}° ${t('sidereal')}`, t('eachSpan'), localizedTerm(cosmic.nakshatra_name)],
    [t('yoga'), t('sunMoonNormalized'), t('angleSpan'), localizedTerm(cosmic.yoga_name)],
    [t('karana'), t('tithiHalves'), t('elongationHalf'), localizedTerm(cosmic.karana_name)],
  ].map(([label, line, formula, result]) => `<article class="cosmic-fact"><span>${label}</span><p>${line}</p><code>${formula}</code><strong>${result}</strong></article>`).join('');
  $('#planet-table-body').innerHTML = cosmic.planets.map((planet) => `<tr data-planet="${planet.name}"><td><b class="planet-symbol">${planet.symbol}</b>${localizedTerm(planet.name)}</td><td>${planet.longitude.toFixed(2)}°</td><td>${localizedTerm(planet.rashi)}</td><td>${localizedTerm(planet.nakshatra)}</td><td>${planet.pada}</td><td class="${planet.retrograde ? 'retrograde' : ''}">${planet.retrograde ? t('retrograde') : t('direct')}</td><td>${planet.speed.toFixed(3)}${t('perDay')}</td></tr>`).join('');
  $('#planet-table-body').querySelectorAll('tr').forEach((row) => {
    const planet = cosmic.planets.find((item) => item.name === row.dataset.planet);
    row.tabIndex = 0;
    row.addEventListener('click', () => openPlanetDrawer(planet, row));
    row.addEventListener('keydown', (event) => { if (event.key === 'Enter' || event.key === ' ') openPlanetDrawer(planet, row); });
  });
  $('#transition-list').innerHTML = cosmic.planets.filter((planet) => planet.name === 'Moon' || planet.name === 'Sun').map((planet, index) => `<article class="transition"><span class="transition-count">${index ? t('nextTithi') : '2 घंटे 12 मिनट में'}</span><strong>${index ? `${t('tithiBoundary')} · ${localizedTerm(cosmic.tithi_name)}` : `${t('moonEnters')} ${localizedTerm(nakshatraNames[(nakshatraNames.indexOf(planet.nakshatra) + 1) % 27])}`}</strong><time>${formatDate(state.panchanga?.date)} · ${index ? t('laterToday') : '18:22'}</time></article>`).join('');
  updateSolarSystem(cosmic);
  if (state.selectedPlanet) {
    const selected = cosmic.planets.find((planet) => planet.name === state.selectedPlanet);
    const selectedMark = selected && document.querySelector(`.planet-mark[data-planet="${selected.name}"]`);
    if (selected && selectedMark) openPlanetDrawer(selected, selectedMark);
  }
}

function openPlanetDrawer(planet, source) {
  state.selectedPlanet = planet.name;
  const drawer = $('#planet-drawer');
  const isHindi = state.language === 'hi';
  const labels = isHindi
    ? { longitude: 'देशांतर', rashi: 'राशि', nakshatra: 'नक्षत्र', pada: 'पद', motion: 'गति', speed: 'वेग', lord: 'स्वामी', element: 'तत्व', status: 'स्थिति', ingress: 'अगली राशि', nextNakshatra: 'अगला नक्षत्र' }
    : { longitude: 'Longitude', rashi: 'Rashi', nakshatra: 'Nakshatra', pada: 'Pada', motion: 'Motion', speed: 'Speed', lord: 'Lord', element: 'Element', status: 'Status', ingress: 'Next Rashi', nextNakshatra: 'Next Nakshatra' };
  const rashiLords = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter'];
  const elements = ['Fire', 'Earth', 'Air', 'Water'];
  const rashiIndex = Math.floor(planet.longitude / 30);
  const nakshatraIndex = nakshatraNames.indexOf(planet.nakshatra);
  const speed = Math.abs(planet.speed) || 0.001;
  const distanceToRashi = planet.speed >= 0 ? 30 - (planet.longitude % 30) : planet.longitude % 30;
  const daysToRashi = distanceToRashi / speed;
  $('#drawer-planet-name').textContent = `${planet.symbol} ${localizedTerm(planet.name)}`;
  $('#drawer-planet-summary').textContent = `${planet.longitude.toFixed(2)}° · ${localizedTerm(planet.rashi)} · ${localizedTerm(planet.nakshatra)}`;
  $('#drawer-planet-grid').innerHTML = [
    [labels.longitude, `${planet.longitude.toFixed(3)}°`], [labels.rashi, localizedTerm(planet.rashi)],
    [labels.nakshatra, localizedTerm(planet.nakshatra)], [labels.pada, planet.pada],
    [labels.motion, planet.retrograde ? t('retrograde') : t('direct')], [labels.speed, `${planet.speed.toFixed(3)}°/day`],
    [labels.lord, localizedTerm(rashiLords[rashiIndex])], [labels.element, isHindi ? { Fire: 'अग्नि', Earth: 'पृथ्वी', Air: 'वायु', Water: 'जल' }[elements[rashiIndex % 4]] : elements[rashiIndex % 4]],
    [labels.status, planet.retrograde ? t('retrograde') : t('direct')], [labels.ingress, `${localizedTerm(rashiNames[(rashiIndex + (planet.speed >= 0 ? 1 : 11)) % 12])} · ~${daysToRashi.toFixed(1)}d`],
    [labels.nextNakshatra, `${localizedTerm(nakshatraNames[(nakshatraIndex + (planet.speed >= 0 ? 1 : 26)) % 27])}`],
  ].map(([label, value]) => `<div><span>${label}</span><strong>${value}</strong></div>`).join('');
  $('#drawer-planet-education').textContent = isHindi
    ? `${localizedTerm(planet.name)} की यह स्थिति निरयन देशांतर से निकाली गई है। गति बदलने पर यह प्रोफ़ाइल और आकाश चक्र तुरंत अपडेट होता है।`
    : `${planet.name} is positioned from its sidereal longitude. This profile and the sky wheel update immediately as playback changes.`;
  drawer.hidden = false;
  document.querySelectorAll('.planet-mark,.planet-table tr').forEach((item) => item.classList.remove('selected-planet'));
  source.classList.add('selected-planet');
}

function updateSolarSystem(cosmic) {
  const positions = Object.fromEntries(cosmic.planets.map((planet) => [planet.name, planet.longitude]));
  positions.Earth = (positions.Sun + 180) % 360;
  ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn'].forEach((body) => {
    const orbit = document.querySelector(`.orbit[data-body="${body}"]`);
    if (!orbit || !orbit.clientWidth) return;
    const label = orbit.querySelector('i');
    const radius = Math.min(orbit.clientWidth, orbit.clientHeight) / 2;
    const angle = positions[body] || 0;
    label.style.transform = `translate(-50%, -50%) rotate(${angle}deg) translateY(-${radius}px) rotate(${-angle}deg)`;
    label.dataset.longitude = `${angle.toFixed(2)}°`;
  });
}

function showPlanetTooltip(planet, mark) {
  const tooltip = $('#planet-tooltip');
  tooltip.hidden = false;
  tooltip.innerHTML = `<b>${planet.symbol} ${localizedTerm(planet.name)}</b><strong>${planet.longitude.toFixed(2)}° · ${localizedTerm(planet.rashi)}</strong><span>${localizedTerm(planet.nakshatra)} · ${state.language === 'hi' ? 'पद' : 'Pada'} ${planet.pada}</span><span>${planet.retrograde ? t('retrograde') : t('direct')} · ${planet.speed.toFixed(2)}°/day</span>`;
  const box = mark.getBoundingClientRect();
  const parent = $('#zodiac-wheel').getBoundingClientRect();
  tooltip.style.left = `${box.left - parent.left + 14}px`;
  tooltip.style.top = `${box.top - parent.top - 12}px`;
}

function syncUrl() {
  const { latitude, longitude, elevation, timezone } = state.location;
  const query = new URLSearchParams({ lat: latitude, lon: longitude, elevation, tz: timezone, lang: state.language });
  history.replaceState(null, '', `${location.pathname}?${query}`);
}

function syncInputs() {
  $('#latitude').value = state.location.latitude;
  $('#longitude').value = state.location.longitude;
  $('#elevation').value = state.location.elevation;
  $('#timezone').value = state.location.timezone;
}

async function request(path) {
  const response = await fetch(path);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || 'Request failed');
  return data;
}

function showLoading() {
  $('#fact-grid').innerHTML = Array.from({ length: 4 }, () => '<article class="fact skeleton" aria-label="Loading calculation"></article>').join('');
  $('#brahma-window').textContent = t('calculating');
  $('#rahu-window').textContent = t('calculating');
}

async function calculate() {
  const { latitude, longitude, elevation, timezone } = state.location;
  const query = new URLSearchParams({ latitude, longitude, elevation, timezone });
  $('#banner').textContent = t('calculatingLocation');
  $('.status-dot').textContent = t('calculating');
  showLoading();
  try {
    state.panchanga = await request(`/panchanga/calculate?${query}`);
    state.cosmic = await request('/panchanga/cosmic');
    await loadFestivalMonths(state.panchanga.date);
    $('#banner').textContent = `${t('liveCalculation')} · ${calculationDateLine(state.panchanga.date, timezone)}. ${t('locationLinkNote')}`;
    $('#banner').classList.remove('banner-error');
    $('#location-label').textContent = t('selectedLocation');
    $('#location-card-name').textContent = t('selectedLocation');
    $('.status-dot').textContent = t('liveCalculation');
    $('#location-coordinates').textContent = `${Math.abs(latitude).toFixed(4)}° ${latitude < 0 ? 'S' : 'N'} · ${Math.abs(longitude).toFixed(4)}° ${longitude < 0 ? 'W' : 'E'} · ${Math.round(elevation)} m`;
    $('#location-timezone').textContent = timezone;
    syncUrl();
    render();
  } catch (error) {
    $('#banner').textContent = `${state.language === 'hi' ? 'गणना नहीं हो सकी' : 'Unable to calculate'}: ${error.message}`;
    $('#banner').classList.add('banner-error');
    $('.status-dot').textContent = 'Calculation failed';
  }
}

function loadLocationFromUrl() {
  const query = new URLSearchParams(location.search);
  const latitude = query.has('lat') ? Number(query.get('lat')) : null;
  const longitude = query.has('lon') ? Number(query.get('lon')) : null;
  const elevation = query.has('elevation') ? Number(query.get('elevation')) : null;
  const timezone = query.get('tz');
  const language = query.get('lang');
  if (Number.isFinite(latitude) && latitude >= -90 && latitude <= 90) state.location.latitude = latitude;
  if (Number.isFinite(longitude) && longitude >= -180 && longitude <= 180) state.location.longitude = longitude;
  if (Number.isFinite(elevation) && elevation >= -500 && elevation <= 10000) state.location.elevation = elevation;
  if (timezone) state.location.timezone = timezone;
  if (language === 'en' || language === 'hi') state.language = language;
}

function showSettingsMessage(message) {
  $('#settings-message').textContent = message;
}

function applyLanguage() {
  document.documentElement.lang = state.language;
  $('nav').setAttribute('aria-label', t('mainNavigation'));
  $('.language-switch').setAttribute('aria-label', t('language'));
  document.querySelectorAll('[data-i18n]').forEach((element) => { element.textContent = t(element.dataset.i18n); });
  $('.location-card .eyebrow').textContent = t('calculationLocation');
  $('.timeline-heading span:first-child').textContent = t('localTimeWindows');
  $('.section-heading .eyebrow').textContent = t('todaysPanchanga');
  $('.festival-section .eyebrow').textContent = t('comingCelebrations');
  $('.quick-card .eyebrow').textContent = t('liveDetails');
  $('.timeline-details summary').textContent = t('solarDailyWindows');
  $('.clock-view-label').textContent = t('liveLocalTime');
  $('#location-heading').textContent = t('calculateForLocation');
  $('#settings > .eyebrow').textContent = t('locationCalibration');
  $('#panchanga > .eyebrow').textContent = t('todaysPanchanga');
  $('#calendar .eyebrow').textContent = t('panIndianObservances');
  $('#calendar-note').textContent = t('calendarNote');
  $('#festival-heading').textContent = t('comingFestivals');
  $('.festival-section .text-link').textContent = t('calendar');
  $('#solar-card-title').textContent = `${t('sunrise')} & ${t('sunset')}`;
  $('#lunar-card-title').textContent = `${t('moonrise')} & ${t('moonset')}`;
  $('#brahma-card-title').textContent = t('brahmaMuhurta');
  $('#rahu-card-title').textContent = t('rahuKaal');
  document.querySelectorAll('.card-link').forEach((button) => { button.textContent = `${t('viewDetails')} ›`; });
  $('.location-search').textContent = t('changeLocation');
  document.querySelectorAll('.quick-stats small').forEach((element, index) => {
    element.textContent = t(['sunrise', 'sunset', 'moonrise', 'moonset'][index]);
  });
  document.querySelectorAll('.settings-form label span[data-i18n]').forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  $('#device-location').textContent = t('useDeviceLocation');
  $('#share-location').textContent = t('copyShareLink');
  $('#location-form button[type="submit"]').textContent = t('recalculate');
  $('#previous-month').setAttribute('aria-label', state.language === 'hi' ? 'पिछला महीना' : 'Previous month');
  $('#next-month').setAttribute('aria-label', state.language === 'hi' ? 'अगला महीना' : 'Next month');
  document.querySelectorAll('.weekday-row span').forEach((element, index) => { element.textContent = translations[state.language].weekdays[index]; });
  document.querySelectorAll('.telemetry div span').forEach((element, index) => {
    element.textContent = t(['sunrise', 'sunset', 'moonrise', 'moonset'][index]);
  });
  $('#calendar-today').textContent = t('todayButton');
  $('#refresh-calculation').setAttribute('aria-label', t('recalculate'));
  $('#refresh-calculation').title = t('recalculate');
  document.querySelectorAll('[data-language]').forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.language === state.language));
  });
}

document.querySelectorAll('[data-view]').forEach((button) => button.addEventListener('click', () => {
  document.querySelectorAll('.nav').forEach((item) => item.classList.remove('active'));
  if (button.classList.contains('nav')) button.classList.add('active');
  document.querySelectorAll('.view').forEach((view) => view.classList.remove('active'));
  $(`#${button.dataset.view}`).classList.add('active');
  if (button.dataset.view === 'calendar') renderFestivals();
  if (button.dataset.view === 'cosmos') renderCosmos();
}));

$('#location-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  state.location = {
    latitude: Number($('#latitude').value), longitude: Number($('#longitude').value),
    elevation: Number($('#elevation').value || 0), timezone: $('#timezone').value.trim(),
  };
  await calculate();
  if (state.panchanga) document.querySelector('[data-view="dashboard"]').click();
});

$('#device-location').addEventListener('click', () => {
  if (!navigator.geolocation) return showSettingsMessage('Device location is not available in this browser.');
  showSettingsMessage('Requesting device location…');
  navigator.geolocation.getCurrentPosition((position) => {
    state.location.latitude = position.coords.latitude;
    state.location.longitude = position.coords.longitude;
    state.location.elevation = position.coords.altitude || 0;
    state.location.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    syncInputs();
    showSettingsMessage('Location loaded. Recalculate to update the reading.');
  }, () => showSettingsMessage('Unable to read device location. Enter coordinates manually.'));
});

$('#share-location').addEventListener('click', async () => {
  syncUrl();
  try {
    await navigator.clipboard.writeText(location.href);
    showSettingsMessage('Share link copied.');
  } catch {
    showSettingsMessage(`Share this link: ${location.href}`);
  }
});

$('#refresh-calculation').addEventListener('click', calculate);
document.querySelectorAll('[data-language]').forEach((button) => button.addEventListener('click', () => {
  state.language = button.dataset.language;
  applyLanguage();
  render();
  syncUrl();
}));
$('#previous-month').addEventListener('click', () => changeCalendarMonth(-1));
$('#next-month').addEventListener('click', () => changeCalendarMonth(1));
$('#calendar-today').addEventListener('click', () => {
  const parts = wallParts(state.panchanga?.date);
  if (!parts) return;
  state.calendarMonth = { year: parts.year, month: parts.month };
  renderFestivals();
});

$('#cosmos-slider').addEventListener('input', async (event) => {
  const offset = Number(event.target.value);
  const selected = new Date(Date.now() + offset * 86400000);
  $('#playback-label').textContent = offset === 0 ? 'Now' : `${offset > 0 ? '+' : ''}${offset} days from now`;
  state.cosmic = await request(`/panchanga/cosmic?at=${encodeURIComponent(selected.toISOString().slice(0, 19))}`);
  renderCosmos();
});
$('#solar-toggle').addEventListener('click', () => {
  const model = $('#solar-orbits');
  model.hidden = !model.hidden;
  $('#solar-toggle').textContent = model.hidden ? t('showOrbitModel') : t('hideOrbitModel');
  if (!model.hidden) requestAnimationFrame(() => updateSolarSystem(state.cosmic));
});
$('#close-planet-drawer').addEventListener('click', () => { state.selectedPlanet = null; $('#planet-drawer').hidden = true; });

loadLocationFromUrl();
syncInputs();
applyLanguage();
render();
setClock();
setInterval(setClock, 1000);
calculate();
