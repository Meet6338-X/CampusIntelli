/**
 * Admin Management Module
 * CRUD operations for Events, Announcements, and Timetable
 * Available for Admin and Faculty roles
 */

const AdminManager = {
    currentUser: null,

    init(user) {
        this.currentUser = user;
        this.setupEventListeners();
    },

    canManage() {
        return this.currentUser && ['admin', 'faculty'].includes(this.currentUser.role);
    },

    isAdmin() {
        return this.currentUser && this.currentUser.role === 'admin';
    },

    setupEventListeners() {
        // Modal close buttons
        document.querySelectorAll('.modal-close, .modal-overlay').forEach(el => {
            el.addEventListener('click', (e) => {
                if (e.target.classList.contains('modal-close') || e.target.classList.contains('modal-overlay')) {
                    this.closeAllModals();
                }
            });
        });
    },

    closeAllModals() {
        document.querySelectorAll('.admin-modal').forEach(m => m.classList.remove('active'));
    },

    showToast(message, type = 'success') {
        // Remove any existing toast
        document.querySelectorAll('.toast').forEach(t => t.remove());

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    },

    // ==========================================
    // EVENTS MANAGEMENT
    // ==========================================

    async loadEvents(container) {
        if (!container) return;

        try {
            const { events } = await API.calendar.getEvents({ include_past: this.isAdmin() });

            let html = `
                <div class="management-header">
                    <h2>Events Management</h2>
                    ${this.canManage() ? '<button class="btn btn-primary" onclick="AdminManager.showEventForm()">+ Add Event</button>' : ''}
                </div>
                <div class="items-grid">
            `;

            if (events.length === 0) {
                html += '<p class="empty-state">No events found</p>';
            } else {
                events.forEach(event => {
                    const isPast = new Date(event.end_date || event.start_date) < new Date();
                    html += `
                        <div class="item-card ${isPast ? 'past-item' : ''}" data-id="${event.id}">
                            <div class="item-header">
                                <span class="item-type badge badge-${event.event_type}">${event.event_type}</span>
                                ${event.is_holiday ? '<span class="badge badge-warning">Holiday</span>' : ''}
                                ${isPast ? '<span class="badge badge-muted">Past</span>' : ''}
                            </div>
                            <h3>${event.title}</h3>
                            <p class="item-desc">${event.description || 'No description'}</p>
                            <div class="item-meta">
                                <span>📅 ${event.start_date}${event.end_date !== event.start_date ? ' - ' + event.end_date : ''}</span>
                                ${event.location ? '<span>📍 ' + event.location + '</span>' : ''}
                            </div>
                            ${this.canManage() ? `
                                <div class="item-actions">
                                    <button class="btn btn-sm btn-ghost" onclick="AdminManager.editEvent('${event.id}')">Edit</button>
                                    ${this.isAdmin() ? `<button class="btn btn-sm btn-danger" onclick="AdminManager.deleteEvent('${event.id}')">Delete</button>` : ''}
                                </div>
                            ` : ''}
                        </div>
                    `;
                });
            }

            html += '</div>';
            container.innerHTML = html;

        } catch (error) {
            container.innerHTML = `<p class="error">Failed to load events: ${error.message}</p>`;
        }
    },

    showEventForm(event = null) {
        const isEdit = !!event;
        const modal = document.createElement('div');
        modal.className = 'admin-modal active';
        modal.id = 'event-modal';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <button class="modal-close">&times;</button>
                <h2>${isEdit ? 'Edit Event' : 'Create New Event'}</h2>
                <form id="event-form" class="admin-form">
                    <input type="hidden" name="id" value="${event?.id || ''}">
                    <div class="form-group">
                        <label>Title *</label>
                        <input type="text" name="title" value="${event?.title || ''}" required>
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <textarea name="description" rows="3">${event?.description || ''}</textarea>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Event Type</label>
                            <select name="event_type">
                                <option value="general" ${event?.event_type === 'general' ? 'selected' : ''}>General</option>
                                <option value="academic" ${event?.event_type === 'academic' ? 'selected' : ''}>Academic</option>
                                <option value="cultural" ${event?.event_type === 'cultural' ? 'selected' : ''}>Cultural</option>
                                <option value="sports" ${event?.event_type === 'sports' ? 'selected' : ''}>Sports</option>
                                <option value="holiday" ${event?.event_type === 'holiday' ? 'selected' : ''}>Holiday</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>
                                <input type="checkbox" name="is_holiday" ${event?.is_holiday ? 'checked' : ''}> Mark as Holiday
                            </label>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Start Date *</label>
                            <input type="date" name="start_date" value="${event?.start_date || ''}" required>
                        </div>
                        <div class="form-group">
                            <label>End Date</label>
                            <input type="date" name="end_date" value="${event?.end_date || ''}">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Start Time</label>
                            <input type="time" name="start_time" value="${event?.start_time || ''}">
                        </div>
                        <div class="form-group">
                            <label>End Time</label>
                            <input type="time" name="end_time" value="${event?.end_time || ''}">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Location</label>
                        <input type="text" name="location" value="${event?.location || ''}" placeholder="Main Auditorium">
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-ghost" onclick="AdminManager.closeAllModals()">Cancel</button>
                        <button type="submit" class="btn btn-primary">${isEdit ? 'Update' : 'Create'} Event</button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(modal);

        modal.querySelector('#event-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            data.is_holiday = formData.has('is_holiday');

            try {
                if (isEdit) {
                    await API.calendar.updateEvent(data.id, data);
                    this.showToast('Event updated successfully');
                } else {
                    await API.calendar.createEvent(data);
                    this.showToast('Event created successfully');
                }
                this.closeAllModals();
                this.loadEvents(document.querySelector('#events-container'));
            } catch (error) {
                this.showToast(error.message, 'error');
            }
        });
    },

    async editEvent(id) {
        try {
            const { event } = await API.calendar.getEvent(id);
            this.showEventForm(event);
        } catch (error) {
            this.showToast('Failed to load event', 'error');
        }
    },

    async deleteEvent(id) {
        if (!confirm('Are you sure you want to delete this event?')) return;

        try {
            await API.calendar.deleteEvent(id);
            this.showToast('Event deleted successfully');
            this.loadEvents(document.querySelector('#events-container'));
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // ==========================================
    // ANNOUNCEMENTS MANAGEMENT
    // ==========================================

    async loadAnnouncements(container) {
        if (!container) return;

        try {
            const { announcements } = await API.announcements.getAll();

            let html = `
                <div class="management-header">
                    <h2>Announcements Management</h2>
                    ${this.canManage() ? '<button class="btn btn-primary" onclick="AdminManager.showAnnouncementForm()">+ Add Announcement</button>' : ''}
                </div>
                <div class="items-list">
            `;

            if (announcements.length === 0) {
                html += '<p class="empty-state">No announcements found</p>';
            } else {
                announcements.forEach(ann => {
                    html += `
                        <div class="item-card announcement-card" data-id="${ann.id}">
                            <div class="item-header">
                                <span class="item-priority badge badge-${ann.priority || 'normal'}">${ann.priority || 'Normal'}</span>
                                ${ann.is_pinned ? '<span class="badge badge-pinned">📌 Pinned</span>' : ''}
                                <span class="item-date">${new Date(ann.created_at || ann.published_at).toLocaleDateString()}</span>
                            </div>
                            <h3>${ann.title}</h3>
                            <p class="item-desc">${ann.content}</p>
                            <div class="item-meta">
                                <span>By: ${ann.created_by_name || 'Admin'}</span>
                                ${ann.target_audience ? '<span>For: ' + ann.target_audience + '</span>' : ''}
                            </div>
                            ${this.canManage() ? `
                                <div class="item-actions">
                                    <button class="btn btn-sm btn-ghost" onclick="AdminManager.editAnnouncement('${ann.id}')">Edit</button>
                                    <button class="btn btn-sm btn-danger" onclick="AdminManager.deleteAnnouncement('${ann.id}')">Delete</button>
                                </div>
                            ` : ''}
                        </div>
                    `;
                });
            }

            html += '</div>';
            container.innerHTML = html;

        } catch (error) {
            container.innerHTML = `<p class="error">Failed to load announcements: ${error.message}</p>`;
        }
    },

    showAnnouncementForm(announcement = null) {
        const isEdit = !!announcement;
        const modal = document.createElement('div');
        modal.className = 'admin-modal active';
        modal.id = 'announcement-modal';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <button class="modal-close">&times;</button>
                <h2>${isEdit ? 'Edit Announcement' : 'Create New Announcement'}</h2>
                <form id="announcement-form" class="admin-form">
                    <input type="hidden" name="id" value="${announcement?.id || ''}">
                    <div class="form-group">
                        <label>Title *</label>
                        <input type="text" name="title" value="${announcement?.title || ''}" required>
                    </div>
                    <div class="form-group">
                        <label>Content *</label>
                        <textarea name="content" rows="4" required>${announcement?.content || ''}</textarea>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Priority</label>
                            <select name="priority">
                                <option value="low" ${announcement?.priority === 'low' ? 'selected' : ''}>Low</option>
                                <option value="normal" ${announcement?.priority === 'normal' || !announcement?.priority ? 'selected' : ''}>Normal</option>
                                <option value="high" ${announcement?.priority === 'high' ? 'selected' : ''}>High</option>
                                <option value="urgent" ${announcement?.priority === 'urgent' ? 'selected' : ''}>Urgent</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Target Audience</label>
                            <select name="target_audience">
                                <option value="all" ${announcement?.target_audience === 'all' || !announcement?.target_audience ? 'selected' : ''}>All</option>
                                <option value="students" ${announcement?.target_audience === 'students' ? 'selected' : ''}>Students Only</option>
                                <option value="faculty" ${announcement?.target_audience === 'faculty' ? 'selected' : ''}>Faculty Only</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="checkbox-label">
                            <input type="checkbox" name="is_pinned" ${announcement?.is_pinned ? 'checked' : ''}>
                            Pin this announcement (appears at top)
                        </label>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-ghost" onclick="AdminManager.closeAllModals()">Cancel</button>
                        <button type="submit" class="btn btn-primary">${isEdit ? 'Update' : 'Create'} Announcement</button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(modal);

        modal.querySelector('#announcement-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            data.is_pinned = formData.has('is_pinned');

            try {
                if (isEdit) {
                    await API.announcements.update(data.id, data);
                    this.showToast('Announcement updated successfully');
                } else {
                    await API.announcements.create(data);
                    this.showToast('Announcement created successfully');
                }
                this.closeAllModals();
                this.loadAnnouncements(document.querySelector('#announcements-container'));
            } catch (error) {
                this.showToast(error.message, 'error');
            }
        });
    },

    async editAnnouncement(id) {
        try {
            const { announcement } = await API.announcements.getById(id);
            if (announcement) {
                this.showAnnouncementForm(announcement);
            }
        } catch (error) {
            this.showToast('Failed to load announcement', 'error');
        }
    },

    async deleteAnnouncement(id) {
        if (!confirm('Are you sure you want to delete this announcement?')) return;

        try {
            await API.announcements.delete(id);
            this.showToast('Announcement deleted successfully');
            this.loadAnnouncements(document.querySelector('#announcements-container'));
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // ==========================================
    // TIMETABLE MANAGEMENT
    // ==========================================

    async loadTimetable(container) {
        if (!container) return;

        try {
            const { timetable } = await API.calendar.getTimetable();
            const { courses } = await API.courses.getAll();

            const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

            let html = `
                <div class="management-header">
                    <h2>Timetable Management</h2>
                    ${this.canManage() ? `
                        <div class="header-actions">
                            <button class="btn btn-primary" onclick="AdminManager.showTimetableForm()">
                                <span class="btn-icon">➕</span> Create New Slot
                            </button>
                            <button class="btn btn-secondary" onclick="AdminManager.showBulkTimetableForm()">
                                <span class="btn-icon">📋</span> Bulk Edit
                            </button>
                        </div>
                    ` : ''}
                </div>
                <div class="timetable-toolbar">
                    <span class="toolbar-info">📅 Weekly Class Schedule</span>
                    <span class="toolbar-stats">${timetable.length} class slots</span>
                </div>
                <div class="timetable-grid">
            `;

            // Group by day
            days.forEach((day, dayIndex) => {
                const daySlots = timetable.filter(s => s.day_of_week === dayIndex);
                daySlots.sort((a, b) => a.start_time.localeCompare(b.start_time));

                html += `
                    <div class="day-column">
                        <div class="day-header">
                            ${day}
                            ${this.canManage() ? `<button class="btn-add-day" onclick="AdminManager.showTimetableForm({day_of_week: ${dayIndex}})" title="Add class on ${day}">+</button>` : ''}
                        </div>
                        <div class="day-slots">
                `;

                if (daySlots.length === 0) {
                    html += `
                        <div class="empty-slot">
                            <span>No classes</span>
                            ${this.canManage() ? `<button class="btn btn-sm btn-ghost" onclick="AdminManager.showTimetableForm({day_of_week: ${dayIndex}})">+ Add Class</button>` : ''}
                        </div>
                    `;
                } else {
                    daySlots.forEach(slot => {
                        html += `
                            <div class="time-slot" data-id="${slot.id}">
                                <div class="slot-time">${slot.start_time} - ${slot.end_time}</div>
                                <div class="slot-course">${slot.course_code || ''} ${slot.course_name}</div>
                                <div class="slot-meta">
                                    <span>📍 ${slot.room || 'TBA'}</span>
                                    <span class="slot-type badge badge-${slot.slot_type}">${slot.slot_type}</span>
                                </div>
                                ${this.canManage() ? `
                                    <div class="slot-actions">
                                        <button class="btn btn-sm btn-ghost" onclick="AdminManager.editTimetableSlot('${slot.id}')" title="Edit">✏️ Edit</button>
                                        ${this.isAdmin() ? `<button class="btn btn-sm btn-danger" onclick="AdminManager.deleteTimetableSlot('${slot.id}')" title="Delete">🗑️</button>` : ''}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    });
                }

                html += '</div></div>';
            });

            html += '</div>';
            container.innerHTML = html;

            // Store courses for form
            this._courses = courses;

        } catch (error) {
            container.innerHTML = `<p class="error">Failed to load timetable: ${error.message}</p>`;
        }
    },

    async showTimetableForm(slot = null) {
        // slot can be a full slot object (editing) or just defaults like {day_of_week: 2}
        const isEdit = slot?.id ? true : false;
        const defaults = slot || {};

        // Ensure courses are loaded
        if (!this._courses) {
            const { courses } = await API.courses.getAll();
            this._courses = courses;
        }

        const modal = document.createElement('div');
        modal.className = 'admin-modal active';
        modal.id = 'timetable-modal';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content">
                <button class="modal-close">&times;</button>
                <h2>${isEdit ? 'Edit Class Slot' : 'Create New Class Slot'}</h2>
                <form id="timetable-form" class="admin-form">
                    <input type="hidden" name="id" value="${defaults.id || ''}">
                    <div class="form-group">
                        <label>Course *</label>
                        <select name="course_id" required>
                            <option value="">Select Course</option>
                            ${this._courses.map(c =>
            `<option value="${c.id}" ${defaults.course_id === c.id ? 'selected' : ''}>${c.code} - ${c.name}</option>`
        ).join('')}
                        </select>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Day *</label>
                            <select name="day_of_week" required>
                                <option value="0" ${defaults.day_of_week === 0 ? 'selected' : ''}>Monday</option>
                                <option value="1" ${defaults.day_of_week === 1 ? 'selected' : ''}>Tuesday</option>
                                <option value="2" ${defaults.day_of_week === 2 ? 'selected' : ''}>Wednesday</option>
                                <option value="3" ${defaults.day_of_week === 3 ? 'selected' : ''}>Thursday</option>
                                <option value="4" ${defaults.day_of_week === 4 ? 'selected' : ''}>Friday</option>
                                <option value="5" ${defaults.day_of_week === 5 ? 'selected' : ''}>Saturday</option>
                                <option value="6" ${defaults.day_of_week === 6 ? 'selected' : ''}>Sunday</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Slot Type</label>
                            <select name="slot_type">
                                <option value="lecture" ${defaults.slot_type === 'lecture' ? 'selected' : ''}>Lecture</option>
                                <option value="lab" ${defaults.slot_type === 'lab' ? 'selected' : ''}>Lab</option>
                                <option value="tutorial" ${defaults.slot_type === 'tutorial' ? 'selected' : ''}>Tutorial</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Start Time *</label>
                            <input type="time" name="start_time" value="${defaults.start_time || '09:00'}" required>
                        </div>
                        <div class="form-group">
                            <label>End Time *</label>
                            <input type="time" name="end_time" value="${defaults.end_time || '10:00'}" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Room</label>
                            <input type="text" name="room" value="${defaults.room || ''}" placeholder="Room 101">
                        </div>
                        <div class="form-group">
                            <label>Section</label>
                            <input type="text" name="section" value="${defaults.section || ''}" placeholder="A">
                        </div>
                    </div>
                    <div class="form-actions">
                        <button type="button" class="btn btn-ghost" onclick="AdminManager.closeAllModals()">Cancel</button>
                        <button type="submit" class="btn btn-primary">${isEdit ? 'Update' : 'Create'} Slot</button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(modal);

        modal.querySelector('#timetable-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            data.day_of_week = parseInt(data.day_of_week);

            try {
                if (isEdit) {
                    await API.calendar.updateTimetableSlot(data.id, data);
                    this.showToast('Timetable slot updated');
                } else {
                    await API.calendar.createTimetableSlot(data);
                    this.showToast('Timetable slot created');
                }
                this.closeAllModals();
                // Refresh the main timetable page
                if (typeof App !== 'undefined' && App.loadTimetable) {
                    App.loadTimetable();
                }
            } catch (error) {
                this.showToast(error.message, 'error');
            }
        });
    },

    async editTimetableSlot(id) {
        try {
            const { timetable } = await API.calendar.getTimetable();
            const slot = timetable.find(s => s.id === id);
            if (slot) {
                this.showTimetableForm(slot);
            }
        } catch (error) {
            this.showToast('Failed to load slot', 'error');
        }
    },

    async deleteTimetableSlot(id) {
        if (!confirm('Are you sure you want to delete this class slot?')) return;

        try {
            await API.calendar.deleteTimetableSlot(id);
            this.showToast('Class slot deleted');
            // Refresh the main timetable page
            if (typeof App !== 'undefined' && App.loadTimetable) {
                App.loadTimetable();
            }
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // ==========================================
    // BULK TIMETABLE MANAGEMENT
    // ==========================================

    async showBulkTimetableForm() {
        if (!this._courses) {
            const { courses } = await API.courses.getAll();
            this._courses = courses;
        }

        const { timetable } = await API.calendar.getTimetable();
        const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

        const modal = document.createElement('div');
        modal.className = 'admin-modal active';
        modal.id = 'bulk-timetable-modal';
        modal.innerHTML = `
            <div class="modal-overlay"></div>
            <div class="modal-content modal-lg">
                <button class="modal-close">&times;</button>
                <h2>📋 Bulk Timetable Editor</h2>
                <p class="modal-subtitle">Edit all class slots in one place</p>
                <div class="bulk-timetable-list">
                    ${timetable.length === 0 ? '<p class="empty-state">No timetable slots found. Create some first!</p>' : ''}
                    ${timetable.map(slot => `
                        <div class="bulk-slot-row" data-id="${slot.id}">
                            <div class="bulk-slot-info">
                                <span class="slot-day">${days[slot.day_of_week]}</span>
                                <span class="slot-course">${slot.course_code || ''} ${slot.course_name}</span>
                            </div>
                            <div class="bulk-slot-fields">
                                <input type="time" class="bulk-start" value="${slot.start_time}" title="Start Time">
                                <span>-</span>
                                <input type="time" class="bulk-end" value="${slot.end_time}" title="End Time">
                                <input type="text" class="bulk-room" value="${slot.room || ''}" placeholder="Room" title="Room">
                                <select class="bulk-type" title="Type">
                                    <option value="lecture" ${slot.slot_type === 'lecture' ? 'selected' : ''}>Lecture</option>
                                    <option value="lab" ${slot.slot_type === 'lab' ? 'selected' : ''}>Lab</option>
                                    <option value="tutorial" ${slot.slot_type === 'tutorial' ? 'selected' : ''}>Tutorial</option>
                                </select>
                            </div>
                            <div class="bulk-slot-actions">
                                <button class="btn btn-sm btn-ghost bulk-save" data-id="${slot.id}">💾</button>
                                <button class="btn btn-sm btn-danger bulk-delete" data-id="${slot.id}">🗑️</button>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-ghost" onclick="AdminManager.closeAllModals()">Close</button>
                    <button type="button" class="btn btn-primary" onclick="AdminManager.showTimetableForm()">+ Add New Slot</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Add event listeners for inline editing
        modal.querySelectorAll('.bulk-save').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.dataset.id;
                const row = modal.querySelector(`.bulk-slot-row[data-id="${id}"]`);
                const data = {
                    start_time: row.querySelector('.bulk-start').value,
                    end_time: row.querySelector('.bulk-end').value,
                    room: row.querySelector('.bulk-room').value,
                    slot_type: row.querySelector('.bulk-type').value
                };
                try {
                    await API.calendar.updateTimetableSlot(id, data);
                    this.showToast('Slot updated');
                } catch (error) {
                    this.showToast(error.message, 'error');
                }
            });
        });

        modal.querySelectorAll('.bulk-delete').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.dataset.id;
                if (!confirm('Delete this slot?')) return;
                try {
                    await API.calendar.deleteTimetableSlot(id);
                    modal.querySelector(`.bulk-slot-row[data-id="${id}"]`).remove();
                    this.showToast('Slot deleted');
                } catch (error) {
                    this.showToast(error.message, 'error');
                }
            });
        });
    }
};

// Export for use
window.AdminManager = AdminManager;
