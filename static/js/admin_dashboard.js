class AdminDashboard {
    constructor() {
        this.currentSection = 'dashboard';
        this.init();
    }

    getCSRFToken() {
        // Método 1: Meta tag (novo)
        const metaToken = document.querySelector('meta[name="csrf-token"]');
        if (metaToken) {
            const token = metaToken.getAttribute('content');
            console.log('CSRF token do meta tag:', token);
            return token;
        }
        
        // Método 2: Input hidden
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        if (token) {
            console.log('CSRF token do input:', token.value);
            return token.value;
        }
        
        // Método 3: Cookie
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                console.log('CSRF token do cookie:', value);
                return value;
            }
        }
        
        console.warn('CSRF token não encontrado!');
        return '';
    }

    async apiRequest(url, options = {}) {
        const defaultOptions = {
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': this.getCSRFToken(),
                'Content-Type': 'application/json'
            }
        };
        
        return fetch(url, { ...defaultOptions, ...options });
    }

    init() {
        this.setupNavigation();
        this.setupModals();
        this.updateCurrentDate();
        this.loadDashboardData();
    }

    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.currentTarget.getAttribute('href').substring(1);
                this.showSection(section);
            });
        });
    }

    setupModals() {
        const closeButtons = document.querySelectorAll('.close-modal');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.closeModals();
            });
        });

        const addDogBtn = document.getElementById('add-dog-btn');
        if (addDogBtn) {
            addDogBtn.addEventListener('click', () => {
                this.showDogModal(); // Call without parameters for new dog
            });
        }

        const dogForm = document.getElementById('dog-form');
        if (dogForm) {
            dogForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveDog(e.target);
            });
        }

        // Fechar modal ao clicar no backdrop
        const dogModal = document.getElementById('dog-modal');
        if (dogModal) {
            dogModal.addEventListener('click', (e) => {
                if (e.target === dogModal) {
                    this.closeModals();
                }
            });
        }
    }

    updateCurrentDate() {
        const now = new Date();
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        const dateElement = document.getElementById('current-date');
        if (dateElement) {
            dateElement.textContent = now.toLocaleDateString('pt-BR', options);
        }
    }

    showSection(section) {
        this.currentSection = section;
        
        // Update page title
        const pageTitle = document.getElementById('page-title');
        const titles = {
            'dashboard': 'Dashboard',
            'dogs': 'Gerenciar Cães',
            'adoptions': 'Solicitações de Adoção',
            'volunteers': 'Candidaturas de Voluntário',
            'messages': 'Mensagens de Contato',
            'testimonials': 'Depoimentos'
        };
        if (pageTitle) {
            pageTitle.textContent = titles[section] || 'Dashboard';
        }
        
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('bg-blue-700');
        });
        
        const activeNav = document.querySelector('[href="#' + section + '"]');
        if (activeNav) {
            activeNav.classList.add('bg-blue-700');
        }
        
        document.querySelectorAll('.section').forEach(sec => {
            sec.classList.add('hidden');
        });
        
        const sectionElement = document.getElementById(section + '-section');
        if (sectionElement) {
            sectionElement.classList.remove('hidden');
            
            switch(section) {
                case 'dashboard':
                    this.loadDashboardData();
                    break;
                case 'dogs':
                    this.loadDogsData();
                    break;
                case 'adoptions':
                    this.loadAdoptionsData();
                    break;
                case 'volunteers':
                    this.loadVolunteersData();
                    break;
                case 'messages':
                    this.loadMessagesData();
                    break;
                case 'testimonials':
                    this.loadTestimonialsData();
                    break;
            }
        }
    }

    async loadDashboardData() {
        try {
            const response = await this.apiRequest('/gestao/api/dashboard/');
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            const data = await response.json();
            
            this.updateElement('total-dogs', data.total_dogs);
            this.updateElement('pending-adoptions', data.pending_adoptions);
            this.updateElement('active-volunteers', data.active_volunteers);
            this.updateElement('unread-messages', data.unread_messages);

            this.renderRecentAdoptions(data.recent_adoptions);
            this.renderUrgentMessages(data.urgent_messages);
            
        } catch (error) {
            this.showError('Erro ao carregar dados do dashboard');
        }
    }

    renderUrgentMessages(messages) {
        const container = document.getElementById('urgent-messages');
        if (!container) return;
        
        if (!messages || !messages.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-4">Nenhuma mensagem urgente</p>';
            return;
        }

        let html = '';
        messages.forEach(message => {
            const date = new Date(message.created_at).toLocaleDateString('pt-BR');
            html += '<div class="flex items-center justify-between p-3 bg-red-50 rounded border-l-4 border-red-400">';
            html += '<div>';
            html += '<p class="font-medium text-red-800">' + message.subject + '</p>';
            html += '<p class="text-sm text-red-600">' + message.name + '</p>';
            html += '</div>';
            html += '<span class="text-xs text-red-500">' + date + '</span>';
            html += '</div>';
        });
        container.innerHTML = html;
    }

    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }

    renderRecentAdoptions(adoptions) {
        const container = document.getElementById('recent-adoptions');
        if (!container) return;
        
        if (!adoptions || !adoptions.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-4">Nenhuma adoção recente</p>';
            return;
        }

        let html = '';
        adoptions.forEach(adoption => {
            const date = new Date(adoption.created_at).toLocaleDateString('pt-BR');
            html += '<div class="flex items-center justify-between p-3 bg-gray-50 rounded">';
            html += '<div>';
            html += '<p class="font-medium">' + adoption.dog_name + '</p>';
            html += '<p class="text-sm text-gray-600">' + (adoption.adopter_name || adoption.name || 'Nome não informado') + '</p>';
            html += '</div>';
            html += '<span class="text-xs text-gray-500">' + date + '</span>';
            html += '</div>';
        });
        container.innerHTML = html;
    }

    async loadDogsData() {
        try {
            const response = await this.apiRequest('/gestao/api/dogs/');
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            const dogs = await response.json();
            this.renderDogsTable(dogs);
        } catch (error) {
            this.showError('Erro ao carregar cães');
        }
    }

    renderDogsTable(dogs) {
        const container = document.getElementById('dogs-table');
        if (!container) return;
        
        if (!dogs.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhum cão cadastrado</p>';
            return;
        }

        let html = '<table class="min-w-full bg-white">';
        html += '<thead class="bg-gray-50">';
        html += '<tr>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Foto</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Idade</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Porte</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Destaque</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Interessados</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ações</th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody class="divide-y divide-gray-200">';
        
        dogs.forEach(dog => {
            const photoUrl = dog.photo_url || '/static/images/no-photo.png';
            
            // Formatar idade conforme o modelo Django
            let age = '';
            if (dog.age && dog.age > 0) {
                age = dog.age + ' anos';
                if (dog.age_months && dog.age_months > 0) {
                    age += ' ' + dog.age_months + ' meses';
                }
            } else if (dog.age_months && dog.age_months > 0) {
                age = dog.age_months + ' meses';
            } else {
                age = 'Idade não informada';
            }
            
            // Converter tamanho conforme o modelo Django
            let sizeText = dog.size;
            switch(dog.size) {
                case 'P':
                    sizeText = 'Pequeno';
                    break;
                case 'M':
                    sizeText = 'Médio';
                    break;
                case 'G':
                    sizeText = 'Grande';
                    break;
                default:
                    sizeText = dog.size || 'Não informado';
            }
            
            // Status conforme o modelo Django
            let statusClass = 'bg-blue-100 text-blue-800';
            let statusText = 'Disponível';
            if (dog.status === 'adopted') {
                statusClass = 'bg-green-100 text-green-800';
                statusText = 'Adotado';
            } else if (dog.status === 'pending') {
                statusClass = 'bg-yellow-100 text-yellow-800';
                statusText = 'Adoção Pendente';
            }
            
            html += '<tr>';
            html += '<td class="px-6 py-4 whitespace-nowrap">';
            html += '<img class="h-10 w-10 rounded-full object-cover" src="' + photoUrl + '" alt="' + dog.name + '">';
            html += '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">' + dog.name + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + age + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + sizeText + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap">';
            html += '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ' + statusClass + '">' + statusText + '</span>';
            html += '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">';
            html += '<button onclick="dashboard.toggleDogFeatured(' + dog.id + ')" class="text-yellow-600 hover:text-yellow-900">';
            html += dog.is_featured ? '⭐' : '☆';
            html += '</button>';
            html += '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + (dog.adoption_count || 0) + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">';
            html += '<button onclick="dashboard.editDog(' + dog.id + ')" class="text-indigo-600 hover:text-indigo-900">Editar</button>';
            html += '</td>';
            html += '</tr>';
        });
        
        html += '</tbody>';
        html += '</table>';
        container.innerHTML = html;
    }

    async loadAdoptionsData() {
        try {
            const response = await this.apiRequest('/gestao/api/adoptions/');
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            const adoptions = await response.json();
            this.renderAdoptionsTable(adoptions);
        } catch (error) {
            this.showError('Erro ao carregar adoções');
        }
    }

    renderAdoptionsTable(adoptions) {
        const container = document.getElementById('adoptions-table');
        if (!container) return;
        
        if (!adoptions.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhuma solicitação de adoção</p>';
            return;
        }

        let html = '<table class="min-w-full bg-white">';
        html += '<thead class="bg-gray-50">';
        html += '<tr>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cão</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Data</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ações</th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody class="divide-y divide-gray-200">';
        
        adoptions.forEach(adoption => {
            const date = new Date(adoption.created_at).toLocaleDateString('pt-BR');
            
            // Status conforme o modelo Django
            let statusClass = 'bg-yellow-100 text-yellow-800';
            let statusText = 'Pendente';
            if (adoption.status === 'approved') {
                statusClass = 'bg-green-100 text-green-800';
                statusText = 'Aprovado';
            } else if (adoption.status === 'rejected') {
                statusClass = 'bg-red-100 text-red-800';
                statusText = 'Rejeitado';
            }
            
            html += '<tr>';
            html += '<td class="px-6 py-4 whitespace-nowrap">';
            html += '<div class="flex items-center">';
            html += '<img class="h-8 w-8 rounded-full object-cover mr-2" src="' + (adoption.dog_photo || '/static/images/no-photo.png') + '" alt="' + adoption.dog_name + '">';
            html += '<span class="text-sm font-medium">' + adoption.dog_name + '</span>';
            html += '</div>';
            html += '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">' + adoption.name + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + adoption.email + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap">';
            html += '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ' + statusClass + '">' + statusText + '</span>';
            html += '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + date + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">';
            
            if (adoption.status === 'pending') {
                html += '<button onclick="dashboard.updateAdoptionStatus(' + adoption.id + ', \'approved\')" class="text-green-600 hover:text-green-900 mr-2">Aprovar</button>';
                html += '<button onclick="dashboard.updateAdoptionStatus(' + adoption.id + ', \'rejected\')" class="text-red-600 hover:text-red-900">Rejeitar</button>';
            } else {
                html += '-';
            }
            
            html += '</td>';
            html += '</tr>';
        });
        
        html += '</tbody>';
        html += '</table>';
        container.innerHTML = html;
    }

    async loadVolunteersData() {
        try {
            const response = await this.apiRequest('/gestao/api/volunteers/');
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            const volunteers = await response.json();
            this.renderVolunteersTable(volunteers);
        } catch (error) {
            this.showError('Erro ao carregar voluntários');
        }
    }

    renderVolunteersTable(volunteers) {
        const container = document.getElementById('volunteers-table');
        if (!container) return;
        
        if (!volunteers.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhuma candidatura de voluntário</p>';
            return;
        }

        let html = '<table class="min-w-full bg-white">';
        html += '<thead class="bg-gray-50">';
        html += '<tr>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Idade</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Data</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ações</th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody class="divide-y divide-gray-200">';
        
        volunteers.forEach(volunteer => {
            const date = new Date(volunteer.created_at).toLocaleDateString('pt-BR');
            
            let statusClass = 'bg-yellow-100 text-yellow-800';
            let statusText = 'Pendente';
            if (volunteer.status === 'approved') {
                statusClass = 'bg-green-100 text-green-800';
                statusText = 'Aprovado';
            } else if (volunteer.status === 'rejected') {
                statusClass = 'bg-red-100 text-red-800';
                statusText = 'Rejeitado';
            }
            
            html += '<tr>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">' + volunteer.name + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + volunteer.email + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + volunteer.age + ' anos</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap">';
            html += '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ' + statusClass + '">' + statusText + '</span>';
            html += '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + date + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">';
            html += '<select onchange="dashboard.updateVolunteerStatus(' + volunteer.id + ', this.value)" class="text-sm border rounded px-2 py-1">';
            html += '<option value="pending"' + (volunteer.status === 'pending' ? ' selected' : '') + '>Pendente</option>';
            html += '<option value="approved"' + (volunteer.status === 'approved' ? ' selected' : '') + '>Aprovar</option>';
            html += '<option value="rejected"' + (volunteer.status === 'rejected' ? ' selected' : '') + '>Rejeitar</option>';
            html += '</select>';
            html += '</td>';
            html += '</tr>';
        });
        
        html += '</tbody>';
        html += '</table>';
        container.innerHTML = html;
    }

    async loadMessagesData() {
        try {
            const response = await this.apiRequest('/gestao/api/messages/');
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            const messages = await response.json();
            this.renderMessagesTable(messages);
        } catch (error) {
            this.showError('Erro ao carregar mensagens');
        }
    }

    renderMessagesTable(messages) {
        const container = document.getElementById('messages-table');
        if (!container) return;
        
        if (!messages.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhuma mensagem</p>';
            return;
        }

        let html = '<table class="min-w-full bg-white">';
        html += '<thead class="bg-gray-50">';
        html += '<tr>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Assunto</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Data</th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody class="divide-y divide-gray-200">';
        
        messages.forEach(message => {
            const date = new Date(message.created_at).toLocaleDateString('pt-BR');
            const rowClass = !message.is_read ? 'bg-blue-50' : '';
            
            html += '<tr class="' + rowClass + '">';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">' + message.name + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + message.email + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + message.subject + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + (message.is_read ? 'Lida' : 'Não lida') + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + date + '</td>';
            html += '</tr>';
        });
        
        html += '</tbody>';
        html += '</table>';
        container.innerHTML = html;
    }

    async loadTestimonialsData() {
        try {
            const response = await this.apiRequest('/gestao/api/testimonials/');
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            const testimonials = await response.json();
            this.renderTestimonialsTable(testimonials);
        } catch (error) {
            this.showError('Erro ao carregar depoimentos');
        }
    }

    renderTestimonialsTable(testimonials) {
        const container = document.getElementById('testimonials-table');
        if (!container) return;
        
        if (!testimonials.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhum depoimento</p>';
            return;
        }

        let html = '<table class="min-w-full bg-white">';
        html += '<thead class="bg-gray-50">';
        html += '<tr>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Adotante</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cão</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Depoimento</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Data</th>';
        html += '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ações</th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody class="divide-y divide-gray-200">';
        
        testimonials.forEach(testimonial => {
            const date = new Date(testimonial.created_at).toLocaleDateString('pt-BR');
            const statusClass = testimonial.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800';
            const statusText = testimonial.is_active ? 'Ativo' : 'Inativo';
            const actionText = testimonial.is_active ? 'Desativar' : 'Ativar';
            
            html += '<tr>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">' + testimonial.adopter_name + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + testimonial.dog_name + '</td>';
            html += '<td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">' + testimonial.testimonial + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap">';
            html += '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ' + statusClass + '">' + statusText + '</span>';
            html += '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">' + date + '</td>';
            html += '<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">';
            html += '<button onclick="dashboard.toggleTestimonial(' + testimonial.id + ')" class="text-indigo-600 hover:text-indigo-900">' + actionText + '</button>';
            html += '</td>';
            html += '</tr>';
        });
        
        html += '</tbody>';
        html += '</table>';
        container.innerHTML = html;
    }

    async saveDog(form) {
        try {
            const formData = new FormData(form);
            const dogData = Object.fromEntries(formData.entries());
            
            // Check if we're editing or creating
            const dogId = form.dataset.dogId;
            const isEditing = !!dogId;
            
            // Converter valores para o formato esperado pelo modelo Django
            if (dogData.size) {
                switch(dogData.size) {
                    case 'small':
                        dogData.size = 'P';  // Pequeno
                        break;
                    case 'medium':
                        dogData.size = 'M';  // Médio
                        break;
                    case 'large':
                        dogData.size = 'G';  // Grande
                        break;
                }
            }
            
            // Debug: verificar dados e token
            console.log('Dados do cão (após conversão):', dogData);
            console.log('Is editing:', isEditing);
            console.log('Dog ID:', dogId);
            console.log('CSRF Token:', this.getCSRFToken());
            
            const url = isEditing ? `/gestao/api/dogs/${dogId}/` : '/gestao/api/dogs/';
            const method = isEditing ? 'PUT' : 'POST';
            
            const response = await this.apiRequest(url, {
                method: method,
                body: JSON.stringify(dogData)
            });

            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);

            if (response.ok) {
                const result = await response.json();
                console.log('Resposta de sucesso:', result);
                this.closeModals();
                this.loadDogsData();
                this.showSuccess(isEditing ? 'Cão atualizado com sucesso!' : 'Cão cadastrado com sucesso!');
            } else {
                // Mostrar mais detalhes do erro
                const errorText = await response.text();
                console.error('Erro da API:', errorText);
                console.error('Status completo:', response.status, response.statusText);
                
                if (response.status === 403) {
                    this.showError('Acesso negado. Verifique se você está logado como administrador.');
                } else if (response.status === 401) {
                    this.showError('Você precisa fazer login como administrador.');
                    window.location.href = '/gestao/login/';
                } else if (response.status === 404) {
                    this.showError('Endpoint não encontrado. Verifique se a URL está correta.');
                } else {
                    this.showError('Erro ao salvar cão: ' + response.status + ' - ' + errorText);
                }
            }
        } catch (error) {
            console.error('Erro completo:', error);
            this.showError('Erro ao salvar cão: ' + error.message);
        }
    }

    async updateAdoptionStatus(id, status) {
        try {
            const response = await this.apiRequest('/gestao/api/adoptions/' + id + '/', {
                method: 'PATCH',
                body: JSON.stringify({ status: status })
            });

            if (response.ok) {
                this.loadAdoptionsData();
                this.showSuccess('Status atualizado com sucesso!');
            } else {
                throw new Error('Erro ao atualizar status');
            }
        } catch (error) {
            this.showError('Erro ao atualizar status da adoção');
        }
    }

    async updateVolunteerStatus(id, status) {
        try {
            const response = await this.apiRequest('/gestao/api/volunteers/' + id + '/', {
                method: 'PATCH',
                body: JSON.stringify({ status: status })
            });

            if (response.ok) {
                this.loadVolunteersData();
                this.showSuccess('Status atualizado com sucesso!');
            } else {
                throw new Error('Erro ao atualizar status');
            }
        } catch (error) {
            this.showError('Erro ao atualizar status do voluntário');
        }
    }

    async toggleDogFeatured(id) {
        try {
            const response = await this.apiRequest('/gestao/api/dogs/' + id + '/toggle-featured/', {
                method: 'POST'
            });

            if (response.ok) {
                this.loadDogsData();
                this.showSuccess('Status de destaque atualizado!');
            } else {
                throw new Error('Erro ao atualizar destaque');
            }
        } catch (error) {
            this.showError('Erro ao atualizar destaque do cão');
        }
    }

    async toggleTestimonial(id) {
        try {
            const response = await this.apiRequest('/gestao/api/testimonials/' + id + '/toggle/', {
                method: 'POST'
            });

            if (response.ok) {
                this.loadTestimonialsData();
                this.showSuccess('Status do depoimento atualizado!');
            } else {
                throw new Error('Erro ao atualizar depoimento');
            }
        } catch (error) {
            this.showError('Erro ao atualizar depoimento');
        }
    }

    showDogModal(dog = null) {
        const modal = document.getElementById('dog-modal');
        const modalTitle = document.getElementById('dog-modal-title');
        const form = document.getElementById('dog-form');
        
        if (modal && form) {
            // Reset form
            form.reset();
            
            if (dog) {
                // Editing existing dog
                modalTitle.textContent = 'Editar Cão';
                
                // Fill form with dog data
                form.name.value = dog.name || '';
                form.age.value = dog.age || '';
                form.age_months.value = dog.age_months || '';
                form.gender.value = dog.gender || '';
                
                // Convert size back to form values
                let sizeValue = '';
                switch(dog.size) {
                    case 'P':
                        sizeValue = 'small';
                        break;
                    case 'M':
                        sizeValue = 'medium';
                        break;
                    case 'G':
                        sizeValue = 'large';
                        break;
                }
                form.size.value = sizeValue;
                
                form.breed.value = dog.breed || '';
                form.photo_url.value = dog.photo_url || '';
                form.description.value = dog.description || '';
                form.personality.value = dog.personality || '';
                form.special_needs.value = dog.special_needs || '';
                form.is_featured.checked = dog.is_featured || false;
                
                // Store dog ID for update
                form.dataset.dogId = dog.id;
            } else {
                // Adding new dog
                modalTitle.textContent = 'Adicionar Cão';
                delete form.dataset.dogId;
            }
            
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
    }

    async editDog(dogId) {
        try {
            // First, get the dog data
            const response = await this.apiRequest('/gestao/api/dogs/');
            if (response.ok) {
                const dogs = await response.json();
                const dog = dogs.find(d => d.id === dogId);
                
                if (dog) {
                    this.showDogModal(dog);
                } else {
                    this.showError('Cão não encontrado');
                }
            } else {
                this.showError('Erro ao carregar dados do cão');
            }
        } catch (error) {
            console.error('Erro ao editar cão:', error);
            this.showError('Erro ao editar cão: ' + error.message);
        }
    }

    closeModals() {
        // Corrigido: busca por ID específico ao invés de classe .modal
        const dogModal = document.getElementById('dog-modal');
        if (dogModal) {
            dogModal.classList.add('hidden');
            dogModal.classList.remove('flex');
        }
        
        // Reset form se existir
        const dogForm = document.getElementById('dog-form');
        if (dogForm) {
            dogForm.reset();
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-500' : 'bg-red-500';
        notification.className = 'fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 text-white ' + bgColor;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

let dashboard;
document.addEventListener('DOMContentLoaded', function() {
    dashboard = new AdminDashboard();
});
