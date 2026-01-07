function initializeLayout() {

    // Example layout initialization code
    console.log("Layout initialized");
   const defaultConfig = {
      form_title: "Registro de Incidentes y Lesiones",
      submit_button_text: "Enviar Registro",
      background_color: "#1e3a8a",
      surface_color: "#ffffff",
      text_color: "#374151",
      primary_action_color: "#3b82f6",
      secondary_action_color: "#fbbf24"
    };

    let currentRecordCount = 0;

    const dataHandler = {
      onDataChanged(data) {
        currentRecordCount = data.length;
      }
    };

    async function initializeApp() {
      const dataResult = await window.dataSdk.init(dataHandler);
      if (!dataResult.isOk) {
        console.error("Error al inicializar Data SDK");
      }

      if (window.elementSdk) {
        window.elementSdk.init({
          defaultConfig,
          onConfigChange: async (config) => {
            const titleElement = document.getElementById('formTitle');
            const buttonText = document.getElementById('buttonText');
            
            if (titleElement) {
              titleElement.textContent = config.form_title || defaultConfig.form_title;
            }
            
            if (buttonText) {
              buttonText.textContent = config.submit_button_text || defaultConfig.submit_button_text;
            }

            const bgColor = config.background_color || defaultConfig.background_color;
            const primaryColor = config.primary_action_color || defaultConfig.primary_action_color;
            const accentColor = config.secondary_action_color || defaultConfig.secondary_action_color;
            const textColor = config.text_color || defaultConfig.text_color;
            
            const gradientBg = document.querySelector('.canary-gradient');
            if (gradientBg) {
              gradientBg.style.background = `linear-gradient(135deg, ${bgColor} 0%, ${primaryColor} 50%, ${accentColor} 100%)`;
            }

            const titleGradient = document.getElementById('formTitle');
            if (titleGradient) {
              titleGradient.style.background = `linear-gradient(135deg, ${bgColor} 0%, ${primaryColor} 50%, ${accentColor} 100%)`;
              titleGradient.style.webkitBackgroundClip = 'text';
              titleGradient.style.webkitTextFillColor = 'transparent';
              titleGradient.style.backgroundClip = 'text';
            }

            const labels = document.querySelectorAll('label');
            labels.forEach(label => {
              label.style.color = textColor;
            });

            const submitButton = document.getElementById('submitButton');
            if (submitButton) {
              submitButton.style.background = `linear-gradient(135deg, ${bgColor} 0%, ${primaryColor} 100%)`;
            }

            const inputs = document.querySelectorAll('.input-focus');
            inputs.forEach(input => {
              input.addEventListener('focus', function() {
                this.style.borderColor = primaryColor;
                this.style.boxShadow = `0 0 0 3px ${primaryColor}20`;
              });
            });
          },
          mapToCapabilities: (config) => ({
            recolorables: [
              {
                get: () => config.background_color || defaultConfig.background_color,
                set: (value) => {
                  config.background_color = value;
                  window.elementSdk.setConfig({ background_color: value });
                }
              },
              {
                get: () => config.surface_color || defaultConfig.surface_color,
                set: (value) => {
                  config.surface_color = value;
                  window.elementSdk.setConfig({ surface_color: value });
                }
              },
              {
                get: () => config.text_color || defaultConfig.text_color,
                set: (value) => {
                  config.text_color = value;
                  window.elementSdk.setConfig({ text_color: value });
                }
              },
              {
                get: () => config.primary_action_color || defaultConfig.primary_action_color,
                set: (value) => {
                  config.primary_action_color = value;
                  window.elementSdk.setConfig({ primary_action_color: value });
                }
              },
              {
                get: () => config.secondary_action_color || defaultConfig.secondary_action_color,
                set: (value) => {
                  config.secondary_action_color = value;
                  window.elementSdk.setConfig({ secondary_action_color: value });
                }
              }
            ],
            borderables: [],
            fontEditable: undefined,
            fontSizeable: undefined
          }),
          mapToEditPanelValues: (config) => new Map([
            ["form_title", config.form_title || defaultConfig.form_title],
            ["submit_button_text", config.submit_button_text || defaultConfig.submit_button_text]
          ])
        });
      }
    }

    const form = document.getElementById('incidentForm');
    const submitButton = document.getElementById('submitButton');
    const buttonText = document.getElementById('buttonText');
    const buttonSpinner = document.getElementById('buttonSpinner');
    const successMessage = document.getElementById('successMessage');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      if (currentRecordCount >= 999) {
        successMessage.className = 'success-message mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded';
        successMessage.querySelector('p').textContent = '⚠ Se ha alcanzado el límite máximo de 999 registros. Por favor, elimina algunos registros primero.';
        successMessage.classList.remove('hidden');
        setTimeout(() => {
          successMessage.classList.add('hidden');
        }, 5000);
        return;
      }

      submitButton.disabled = true;
      buttonText.classList.add('hidden');
      buttonSpinner.classList.remove('hidden');

      const formData = {
        nombre: document.getElementById('nombre').value,
        apellidos: document.getElementById('apellidos').value,
        fecha: document.getElementById('fecha').value,
        hora: document.getElementById('hora').value,
        lugar: document.getElementById('lugar').value,
        incidente: document.getElementById('incidente').value,
        descripcion_lesion: document.getElementById('descripcion_lesion').value,
        centro: document.getElementById('centro').value,
        timestamp: new Date().toISOString()
      };

      const result = await window.dataSdk.create(formData);

      submitButton.disabled = false;
      buttonText.classList.remove('hidden');
      buttonSpinner.classList.add('hidden');

      if (result.isOk) {
        successMessage.className = 'success-message mb-6 p-4 bg-green-50 border-l-4 border-green-500 rounded';
        successMessage.querySelector('p').textContent = '✓ Registro enviado correctamente';
        successMessage.classList.remove('hidden');
        form.reset();
        
        setTimeout(() => {
          successMessage.classList.add('hidden');
        }, 5000);
      } else {
        successMessage.className = 'success-message mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded';
        successMessage.querySelector('p').textContent = '✗ Error al enviar el registro. Por favor, intenta de nuevo.';
        successMessage.classList.remove('hidden');
        
        setTimeout(() => {
          successMessage.classList.add('hidden');
        }, 5000);
      }
    });

    initializeApp();

}

// Call the function to initialize the layout
initializeLayout();
