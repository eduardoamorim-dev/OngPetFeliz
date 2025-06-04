// Admin Dashboard JavaScript
class AdminDashboard {
    constructor() {
        this.currentSection = 'dashboard';
        this.init();
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
        // Close modal buttons
        document.querySelectorAll('.close-modal').forEach(btn => {
            btn.addEventListener('click', () => {
                this.closeModals();
            });
        });

        // Add dog button
        document.getElementById('add-dog-btn')?.addEventListener('click', () => {
            this.showDogModal();
        });

        // Dog form submission
        document.getElementById('dog-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveDog(e.target);
        });

        // Click outside modal to close
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('bg-black')) {
                this.closeModals();
            }
        });
    }

    showSection(section) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active', 'bg-blue-700');
        });
        document.querySelector(`[href="#${section}"]`).classList.add('active', 'bg-blue-700');

        // Hide all sections
        document.querySelectorAll('.section').forEach(sec => {
            sec.classList.add('hidden');
        });

        // Show target section
        document.getElementById(`${section}-section`).classList.remove('hidden');

        // Update page title
        const titles = {
            dashboard: 'Dashboard',
            dogs: 'Gerenciar Cães',
            adoptions: 'Solicitações de Adoção',
            volunteers: 'Candidaturas de Voluntário',
            messages: 'Mensagens de Contato',
            testimonials: 'Depoimentos'
        };
        document.getElementById('page-title').textContent = titles[section];

        this.currentSection = section;
        this.loadSectionData(section);
    }

    async loadSectionData(section) {
        this.showLoading();
        
        try {
            switch(section) {
                case 'dashboard':
                    await this.loadDashboardData();
                    break;
                case 'dogs':
                    await this.loadDogsData();
                    break;
                case 'adoptions':
                    await this.loadAdoptionsData();
                    break;
                case 'volunteers':
                    await this.loadVolunteersData();
                    break;
                case 'messages':
                    await this.loadMessagesData();
                    break;
                case 'testimonials':
                    await this.loadTestimonialsData();
                    break;
            }
        } catch (error) {
            this.showError('Erro ao carregar dados: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    async loadDashboardData() {
        try {
            const response = await fetch('/admin/api/dashboard/');
            const data = await response.json();
            
            // Update stats
            document.getElementById('total-dogs').textContent = data.total_dogs;
            document.getElementById('pending-adoptions').textContent = data.pending_adoptions;
            document.getElementById('active-volunteers').textContent = data.active_volunteers;
            document.getElementById('unread-messages').textContent = data.unread_messages;

            // Update recent adoptions
            this.renderRecentAdoptions(data.recent_adoptions);
            
            // Update urgent messages
            this.renderUrgentMessages(data.urgent_messages);
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }

    renderRecentAdoptions(adoptions) {
        const container = document.getElementById('recent-adoptions');
        if (!adoptions.length) {
            container.innerHTML = '<p class="text-gray-500 text-sm">Nenhuma adoção recente</p>';
            return;
        }

        container.innerHTML = adoptions.map(adoption => `
            <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                <img src="${adoption.dog_photo}" alt="${adoption.dog_name}" 
                     class="w-10 h-10 rounded-full object-cover mr-3">
                <div class="flex-1">
                    <p class="font-medium text-sm">${adoption.dog_name}</p>
                    <p class="text-xs text-gray-500">${adoption.adopter_name}</p>
                </div>
                <span class="text-xs px-2 py-1 rounded-full ${this.getStatusClass(adoption.status)}">${this.getStatusText(adoption.status)}</span>
            </div>
        `).join('');
    }

    renderUrgentMessages(messages) {
        const container = document.getElementById('urgent-messages');
        if (!messages.length) {
            container.innerHTML = '<p class="text-gray-500 text-sm">Nenhuma mensagem urgente</p>';
            return;
        }

        container.innerHTML = messages.map(message => `
            <div class="p-3 border-l-4 border-red-500 bg-red-50 rounded">
                <p class="font-medium text-sm">${message.subject}</p>
                <p class="text-xs text-gray-600">${message.name} • ${message.email}</p>
                <p class="text-xs text-gray-500 mt-1">${this.formatDate(message.created_at)}</p>
            </div>
        `).join('');
    }

    async loadDogsData() {
        try {
            const response = await fetch('/admin/api/dogs/');
            const dogs = await response.json();
            this.renderDogsTable(dogs);
        } catch (error) {
            this.showError('Erro ao carregar cães');
        }
    }

    renderDogsTable(dogs) {
        const container = document.getElementById('dogs-table');
        
        if (!dogs.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhum cão cadastrado</p>';
            return;
        }

        container.innerHTML = `
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cão</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Idade</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Raça</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Interesse</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    ${dogs.map(dog => `
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <img class="h-10 w-10 rounded-full object-cover" src="${dog.photo_url || '/static/images/no-photo.png'}" alt="${dog.name}">
                                    <div class="ml-4">
                                        <div class="text-sm font-medium text-gray-900">${dog.name}</div>
                                        <div class="text-sm text-gray-500">${dog.gender === 'M' ? 'Macho' : 'Fêmea'} • ${this.getSizeText(dog.size)}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${this.formatAge(dog.age, dog.age_months)}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${dog.breed || '-'}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${this.getStatusClass(dog.status)}">
                                    ${this.getStatusText(dog.status)}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${dog.adoption_count || 0} solicitações</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <button onclick="adminDashboard.editDog(${dog.id})" class="text-indigo-600 hover:text-indigo-900 mr-3">Editar</button>
                                <button onclick="adminDashboard.toggleFeatured(${dog.id})" class="text-green-600 hover:text-green-900 mr-3">
                                    ${dog.is_featured ? 'Remover Destaque' : 'Destacar'}
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    async loadAdoptionsData() {
        try {
            const response = await fetch('/admin/api/adoptions/');
            const adoptions = await response.json();
            this.renderAdoptionsTable(adoptions);
        } catch (error) {
            this.showError('Erro ao carregar adoções');
        }
    }

    renderAdoptionsTable(adoptions) {
        const container = document.getElementById('adoptions-table');
        
        if (!adoptions.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhuma solicitação de adoção</p>';
            return;
        }

        container.innerHTML = `
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cão</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Candidato</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contato</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    ${adoptions.map(adoption => `
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <img class="h-8 w-8 rounded-full object-cover" src="${adoption.dog_photo}" alt="${adoption.dog_name}">
                                    <div class="ml-3">
                                        <div class="text-sm font-medium text-gray-900">${adoption.dog_name}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">${adoption.name}</div>
                                <div class="text-sm text-gray-500">${adoption.has_experience ? 'Tem experiência' : 'Sem experiência'}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">${adoption.email}</div>
                                <div class="text-sm text-gray-500">${adoption.phone}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${this.getStatusClass(adoption.status)}">
                                    ${this.getStatusText(adoption.status)}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${this.formatDate(adoption.created_at)}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                ${adoption.status === 'pending' ? `
                                    <button onclick="adminDashboard.updateAdoptionStatus(${adoption.id}, 'approved')" 
                                            class="text-green-600 hover:text-green-900 mr-3">Aprovar</button>
                                    <button onclick="adminDashboard.updateAdoptionStatus(${adoption.id}, 'rejected')" 
                                            class="text-red-600 hover:text-red-900">Rejeitar</button>
                                ` : '-'}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    async loadVolunteersData() {
        try {
            const response = await fetch('/admin/api/volunteers/');
            const volunteers = await response.json();
            this.renderVolunteersTable(volunteers);
        } catch (error) {
            this.showError('Erro ao carregar voluntários');
        }
    }

    renderVolunteersTable(volunteers) {
        const container = document.getElementById('volunteers-table');
        
        if (!volunteers.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhuma candidatura de voluntário</p>';
            return;
        }

        container.innerHTML = `
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Candidato</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Idade</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Disponibilidade</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    ${volunteers.map(volunteer => `
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">${volunteer.name}</div>
                                <div class="text-sm text-gray-500">${volunteer.email}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${volunteer.age} anos</td>
                            <td class="px-6 py-4">
                                <div class="text-sm text-gray-900 max-w-xs truncate">${volunteer.availability}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${this.getStatusClass(volunteer.status)}">
                                    ${this.getStatusText(volunteer.status)}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${this.formatDate(volunteer.created_at)}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <button onclick="adminDashboard.viewVolunteer(${volunteer.id})" 
                                        class="text-indigo-600 hover:text-indigo-900 mr-3">Ver</button>
                                ${volunteer.status === 'pending' ? `
                                    <button onclick="adminDashboard.updateVolunteerStatus(${volunteer.id}, 'approved')" 
                                            class="text-green-600 hover:text-green-900 mr-3">Aprovar</button>
                                    <button onclick="adminDashboard.updateVolunteerStatus(${volunteer.id}, 'rejected')" 
                                            class="text-red-600 hover:text-red-900">Rejeitar</button>
                                ` : ''}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    async loadMessagesData() {
        try {
            const response = await fetch('/admin/api/messages/');
            const messages = await response.json();
            this.renderMessagesTable(messages);
        } catch (error) {
            this.showError('Erro ao carregar mensagens');
        }
    }

    renderMessagesTable(messages) {
        const container = document.getElementById('messages-table');
        
        if (!messages.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhuma mensagem</p>';
            return;
        }

        container.innerHTML = `
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Remetente</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Assunto</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Prioridade</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    ${messages.map(message => `
                        <tr class="${!message.is_read ? 'bg-blue-50' : ''}">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">${message.name}</div>
                                <div class="text-sm text-gray-500">${message.email}</div>
                            </td>
                            <td class="px-6 py-4">
                                <div class="text-sm text-gray-900 max-w-xs truncate">${message.subject}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="text-sm ${this.getPriorityClass(message.priority)}">${this.getPriorityText(message.priority)}</span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${message.is_read ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                                    ${message.is_read ? 'Lida' : 'Não Lida'}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${this.formatDate(message.created_at)}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <button onclick="adminDashboard.viewMessage(${message.id})" 
                                        class="text-indigo-600 hover:text-indigo-900 mr-3">Ver</button>
                                <a href="mailto:${message.email}?subject=Re: ${message.subject}" 
                                   class="text-blue-600 hover:text-blue-900">Responder</a>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    async loadTestimonialsData() {
        try {
            const response = await fetch('/admin/api/testimonials/');
            const testimonials = await response.json();
            this.renderTestimonialsTable(testimonials);
        } catch (error) {
            this.showError('Erro ao carregar depoimentos');
        }
    }

    renderTestimonialsTable(testimonials) {
        const container = document.getElementById('testimonials-table');
        
        if (!testimonials.length) {
            container.innerHTML = '<p class="text-gray-500 text-center py-8">Nenhum depoimento</p>';
            return;
        }

        container.innerHTML = `
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Adotante</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cão</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Depoimento</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    ${testimonials.map(testimonial => `
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">${testimonial.adopter_name}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${testimonial.dog_name}</td>
                            <td class="px-6 py-4">
                                <div class="text-sm text-gray-900 max-w-xs truncate">${testimonial.testimonial}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${testimonial.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">
                                    ${testimonial.is_active ? 'Ativo' : 'Inativo'}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                <button onclick="adminDashboard.toggleTestimonial(${testimonial.id})" 
                                        class="text-indigo-600 hover:text-indigo-900">
                                    ${testimonial.is_active ? 'Desativar' : 'Ativar'}
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    // Modal Methods
    showDogModal(dogData = null) {
        const modal = document.getElementById('dog-modal');
        const form = document.getElementById('dog-form');
        const title = document.getElementById('dog-modal-title');
        
        if (dogData) {
            title.textContent = 'Editar Cão';
            this.populateForm(form, dogData);
        } else {
            title.textContent = 'Adicionar Cão';
            form.reset();
        }
        
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }

    closeModals() {
        document.querySelectorAll('[id$="-modal"]').forEach(modal => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        });
    }

    // API Methods
    async saveDog(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.is_featured = formData.has('is_featured');
        
        try {
            this.showLoading();
            const response = await fetch('/admin/api/dogs/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                this.closeModals();
                this.showSuccess('Cão salvo com sucesso!');
                if (this.currentSection === 'dogs') {
                    await this.loadDogsData();
                }
            } else {
                throw new Error('Erro ao salvar cão');
            }
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    async updateAdoptionStatus(id, status) {
        if (!confirm(`Confirmar ${status === 'approved' ? 'aprovação' : 'rejeição'} da adoção?`)) {
            return;
        }

        try {
            this.showLoading();
            const response = await fetch(`/admin/api/adoptions/${id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ status })
            });
            
            if (response.ok) {
                this.showSuccess('Status atualizado com sucesso!');
                await this.loadAdoptionsData();
            } else {
                throw new Error('Erro ao atualizar status');
            }
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    async updateVolunteerStatus(id, status) {
        if (!confirm(`Confirmar ${status === 'approved' ? 'aprovação' : 'rejeição'} do voluntário?`)) {
            return;
        }

        try {
            this.showLoading();
            const response = await fetch(`/admin/api/volunteers/${id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ status })
            });
            
            if (response.ok) {
                this.showSuccess('Status atualizado com sucesso!');
                await this.loadVolunteersData();
            } else {
                throw new Error('Erro ao atualizar status');
            }
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    async toggleFeatured(id) {
        try {
            this.showLoading();
            const response = await fetch(`/admin/api/dogs/${id}/toggle-featured/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });
            
            if (response.ok) {
                this.showSuccess('Status de destaque atualizado!');
                await this.loadDogsData();
            } else {
                throw new Error('Erro ao atualizar destaque');
            }
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    async toggleTestimonial(id) {
        try {
            this.showLoading();
            const response = await fetch(`/admin/api/testimonials/${id}/toggle/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });
            
            if (response.ok) {
                this.showSuccess('Status do depoimento atualizado!');
                await this.loadTestimonialsData();
            } else {
                throw new Error('Erro ao atualizar depoimento');
            }
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    // Utility Methods
    updateCurrentDate() {
        const now = new Date();
        const formatted = now.toLocaleDateString('pt-BR', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        document.getElementById('current-date').textContent = formatted;
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name=csrf-token]')?.content || '';
    }

    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('pt-BR');
    }

    formatAge(years, months) {
        if (years > 0) {
            return months > 0 ? `${years}a ${months}m` : `${years} anos`;
        }
        return `${months} meses`;
    }

    getSizeText(size) {
        const sizes = { small: 'Pequeno', medium: 'Médio', large: 'Grande' };
        return sizes[size] || size;
    }

    getStatusClass(status) {
        const classes = {
            available: 'bg-green-100 text-green-800',
            adopted: 'bg-blue-100 text-blue-800',
            pending: 'bg-yellow-100 text-yellow-800',
            approved: 'bg-green-100 text-green-800',
            rejected: 'bg-red-100 text-red-800'
        };
        return classes[status] || 'bg-gray-100 text-gray-800';
    }

    getStatusText(status) {
        const texts = {
            available: 'Disponível',
            adopted: 'Adotado',
            pending: 'Pendente',
            approved: 'Aprovado',
            rejected: 'Rejeitado'
        };
        return texts[status] || status;
    }

    getPriorityClass(priority) {
        const classes = {
            high: 'text-red-600 font-bold',
            medium: 'text-yellow-600 font-bold',
            normal: 'text-green-600'
        };
        return classes[priority] || 'text-gray-600';
    }

    getPriorityText(priority) {
        const texts = {
            high: '🔴 Alta',
            medium: '🟡 Média',
            normal: '🟢 Normal'
        };
        return texts[priority] || 'Normal';
    }

    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('loading').classList.add('flex');
    }

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('loading').classList.remove('flex');
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    populateForm(form, data) {
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                if (field.type === 'checkbox') {
                    field.checked = data[key];
                } else {
                    field.value = data[key];
                }
            }
        });
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.adminDashboard = new AdminDashboard();
});