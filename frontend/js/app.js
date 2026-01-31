/**
 * CampusIntelli Main Application - Extended version with 20+ modules
 */

const App = {
    user: null,

    // Initialize app
    init() {
        this.checkAuth();
        this.bindEvents();
        this.updateCurrentDate();
    },

    // Update current date display
    updateCurrentDate() {
        const dateEl = document.getElementById('current-date');
        if (dateEl) {
            const now = new Date();
            const options = {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            };
            dateEl.textContent = now.toLocaleDateString('en-US', options);
        }

        // Update greeting name
        const greetingEl = document.getElementById('greeting-name');
        if (greetingEl && this.user) {
            greetingEl.textContent = this.user.name?.split(' ')[0] || 'Student';
        }
    },

    // Check if user is logged in
    checkAuth() {
        const stored = localStorage.getItem('campus_user');
        if (stored) {
            try {
                this.user = JSON.parse(stored);
                this.showMainApp();
            } catch (e) {
                this.showAuthScreen();
            }
        } else {
            this.showAuthScreen();
        }
    },

    // Show auth screen
    showAuthScreen() {
        document.getElementById('auth-screen').classList.add('active');
        document.getElementById('main-app').classList.remove('active');
    },

    // Show main app
    showMainApp() {
        document.getElementById('auth-screen').classList.remove('active');
        document.getElementById('main-app').classList.add('active');

        document.getElementById('user-name').textContent = this.user.name || 'User';
        document.getElementById('user-role').textContent = this.user.role || 'student';

        // Update role badge style
        const roleBadge = document.getElementById('user-role');
        if (roleBadge) {
            roleBadge.classList.remove('admin', 'faculty');
            if (this.user.role === 'admin') {
                roleBadge.classList.add('admin');
            } else if (this.user.role === 'faculty') {
                roleBadge.classList.add('faculty');
            }
        }

        // Show/hide role-specific elements
        this.updateRoleUI();

        // Update date
        this.updateCurrentDate();

        // Load dashboard
        this.loadDashboard();
    },

    // Update UI based on role
    updateRoleUI() {
        const role = this.user?.role || 'student';

        document.querySelectorAll('.faculty-only').forEach(el => {
            el.classList.toggle('hidden', role !== 'faculty' && role !== 'admin');
        });

        document.querySelectorAll('.student-only').forEach(el => {
            el.classList.toggle('hidden', role !== 'student');
        });

        document.querySelectorAll('.admin-only').forEach(el => {
            el.classList.toggle('hidden', role !== 'admin');
        });
    },

    // Bind all events
    bindEvents() {
        // Auth tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
                btn.classList.add('active');
                document.getElementById(`${btn.dataset.tab}-form`).classList.add('active');
            });
        });

        // Login form
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        // Register form
        document.getElementById('register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });

        // Logout
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());

        // Navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateTo(link.dataset.page);
            });
        });

        // Module cards navigation
        document.querySelectorAll('.module-card').forEach(card => {
            card.addEventListener('click', (e) => {
                e.preventDefault();
                if (card.dataset.page) {
                    this.navigateTo(card.dataset.page);
                }
            });
        });

        // Stat cards navigation
        document.querySelectorAll('.stat-card[data-nav]').forEach(card => {
            card.addEventListener('click', () => {
                if (card.dataset.nav) {
                    this.navigateTo(card.dataset.nav);
                }
            });
        });

        // Modal close
        document.querySelector('.modal-close')?.addEventListener('click', () => this.closeModal());
        document.getElementById('modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'modal') this.closeModal();
        });

        // Keyboard navigation for modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });

        // Page-specific buttons
        document.getElementById('add-course-btn')?.addEventListener('click', () => this.showCourseForm());
        document.getElementById('add-assignment-btn')?.addEventListener('click', () => this.showAssignmentForm());
        document.getElementById('generate-qr-btn')?.addEventListener('click', () => this.showQRGenerator());
        document.getElementById('scan-qr-btn')?.addEventListener('click', () => this.showQRScanner());
        document.getElementById('new-booking-btn')?.addEventListener('click', () => this.showBookingForm());
        document.getElementById('new-announcement-btn')?.addEventListener('click', () => this.showAnnouncementForm());
        document.getElementById('new-grievance-btn')?.addEventListener('click', () => this.showGrievanceForm());

        // Profile form
        document.getElementById('profile-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.updateProfile();
        });

        // Feedback form
        document.getElementById('feedback-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.submitFeedback();
        });
    },

    // Handle login
    async handleLogin() {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        try {
            const data = await API.auth.login(email, password);
            this.user = data.user;
            localStorage.setItem('campus_user', JSON.stringify(data.user));
            this.showMainApp();
            this.showToast('Welcome back!', 'success');
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Handle register
    async handleRegister() {
        const userData = {
            name: document.getElementById('reg-name').value,
            email: document.getElementById('reg-email').value,
            password: document.getElementById('reg-password').value,
            role: document.getElementById('reg-role').value,
            department: document.getElementById('reg-dept').value
        };

        try {
            const data = await API.auth.register(userData);
            this.showToast('Account created! Please login.', 'success');
            document.querySelector('[data-tab="login"]').click();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Logout
    logout() {
        localStorage.removeItem('campus_user');
        this.user = null;
        this.showAuthScreen();
        this.showToast('Logged out', 'success');
    },

    // Navigate to page
    navigateTo(page) {
        // Update nav links
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelector(`.nav-link[data-page="${page}"]`)?.classList.add('active');

        // Update pages
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(`page-${page}`)?.classList.add('active');

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Load page data
        switch (page) {
            case 'dashboard': this.loadDashboard(); break;
            case 'academics': this.loadAcademics(); break;
            case 'courses': this.loadCourses(); break;
            case 'assignments': this.loadAssignments(); break;
            case 'attendance': this.loadAttendance(); break;
            case 'examinations': this.loadExaminations(); break;
            case 'timetable': this.loadTimetable(); break;
            case 'fees': this.loadFees(); break;
            case 'bookings': this.loadBookings(); break;
            case 'library': this.loadLibrary(); break;
            case 'events': this.loadEvents(); break;
            case 'announcements': this.loadAnnouncements(); break;
            case 'quiz': this.loadQuizzes(); break;
            case 'feedback': /* Form page, no load needed */ break;
            case 'grievance': this.loadGrievances(); break;
            case 'tpo': this.loadTPO(); break;
            case 'profile': this.loadProfile(); break;
        }
    },

    // Format date nicely
    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        const options = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return date.toLocaleDateString('en-US', options);
    },

    formatShortDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    },

    // ===================
    // DASHBOARD
    // ===================
    async loadDashboard() {
        try {
            // Update greeting
            this.updateCurrentDate();

            // Courses count
            const coursesData = await API.courses.getAll();
            document.getElementById('stat-courses').textContent = coursesData.courses?.length || 0;

            // Assignments
            const assignmentsData = await API.assignments.getAll();
            const pending = assignmentsData.assignments?.filter(a => !a.submitted)?.length || 0;
            document.getElementById('stat-assignments').textContent = pending;

            // Attendance summary
            try {
                const attData = await API.attendance.getSummary();
                const summary = attData.summary || {};
                let total = 0, present = 0;
                Object.values(summary).forEach(v => {
                    total += v.total || 0;
                    present += v.present || 0;
                });
                const pct = total > 0 ? Math.round((present / total) * 100) : 0;
                document.getElementById('stat-attendance').textContent = `${pct}%`;
            } catch (e) {
                document.getElementById('stat-attendance').textContent = '0%';
            }

            // Exams count (mock for now)
            document.getElementById('stat-exams').textContent = '2';

            // Upcoming assignments
            const upcoming = document.getElementById('upcoming-assignments');
            const upcomingList = (assignmentsData.assignments || []).slice(0, 3);
            if (upcomingList.length > 0) {
                upcoming.innerHTML = upcomingList.map(a => `
                    <div class="list-item">
                        <h4>${a.title}</h4>
                        <p>${a.description?.substring(0, 80) || 'No description'}...</p>
                        <span class="date">${this.formatShortDate(a.due_date)}</span>
                    </div>
                `).join('');
            } else {
                upcoming.innerHTML = '<p class="empty-state">No upcoming deadlines</p>';
            }

            // Today's schedule (mock data)
            const schedule = document.getElementById('today-schedule');
            schedule.innerHTML = `
                <div class="list-item">
                    <h4>Data Structures</h4>
                    <p>Room: LH-101 | 09:00 - 10:30</p>
                </div>
                <div class="list-item">
                    <h4>Database Management</h4>
                    <p>Room: LH-203 | 11:00 - 12:30</p>
                </div>
            `;

            // Announcements
            const annData = await API.announcements.getAll();
            const recent = document.getElementById('recent-announcements');
            const recentList = (annData.announcements || []).slice(0, 3);
            if (recentList.length > 0) {
                recent.innerHTML = recentList.map(a => `
                    <div class="list-item">
                        <h4>${a.is_pinned ? '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" style="display:inline;vertical-align:middle;color:var(--warning)"><path d="M12 17v5"/><path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z"/></svg> ' : ''}${a.title}</h4>
                        <p>${a.content?.substring(0, 100)}...</p>
                        <span class="date">${this.formatShortDate(a.published_at)}</span>
                    </div>
                `).join('');
            } else {
                recent.innerHTML = '<p class="empty-state">No announcements</p>';
            }

        } catch (error) {
            console.error('Dashboard load error:', error);
        }
    },

    // ===================
    // ACADEMICS
    // ===================
    async loadAcademics() {
        // Mock data - would come from API
        console.log('Loading academics...');
    },

    // ===================
    // COURSES
    // ===================
    async loadCourses() {
        const container = document.getElementById('courses-list');
        try {
            const data = await API.courses.getAll();
            if (data.courses?.length > 0) {
                container.innerHTML = data.courses.map(c => `
                    <div class="course-card">
                        <h3>${c.code} - ${c.name}</h3>
                        <p>${c.description || 'No description available'}</p>
                        <div class="course-meta">
                            <span>Credits: ${c.credits}</span>
                            <span>Dept: ${c.department}</span>
                        </div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No courses available</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="empty-state">Failed to load courses</p>';
        }
    },

    // ===================
    // ASSIGNMENTS
    // ===================
    async loadAssignments() {
        const container = document.getElementById('assignments-list');
        try {
            const data = await API.assignments.getAll();
            if (data.assignments?.length > 0) {
                container.innerHTML = data.assignments.map(a => `
                    <div class="assignment-card">
                        <h3>${a.title}</h3>
                        <p>${a.description || 'No description'}</p>
                        <div class="assignment-meta">
                            <span>Due: ${this.formatDate(a.due_date)}</span>
                            <span>Max: ${a.max_marks} marks</span>
                        </div>
                        ${a.submitted
                        ? '<span class="badge" style="background: var(--success);">Submitted</span>'
                        : '<span class="badge" style="background: var(--warning);">Pending</span>'}
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No assignments yet</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="empty-state">Failed to load assignments</p>';
        }
    },

    // ===================
    // ATTENDANCE
    // ===================
    async loadAttendance() {
        const container = document.getElementById('attendance-summary');
        try {
            const data = await API.attendance.getSummary();
            const summary = data.summary || {};

            if (Object.keys(summary).length > 0) {
                container.innerHTML = Object.entries(summary).map(([courseId, stats]) => {
                    const percent = stats.total > 0 ? Math.round((stats.present / stats.total) * 100) : 0;
                    return `
                    <div class="attendance-card">
                        <div class="course-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
                        </div>
                        <div class="course-info">
                            <div class="course-name">${courseId.substring(0, 20)}...</div>
                            <div class="attendance-ratio">${stats.present}/${stats.total}</div>
                            <div class="attendance-percent">${percent}% attendance</div>
                        </div>
                    </div>
                    `;
                }).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No attendance records</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="empty-state">Failed to load attendance</p>';
        }
    },

    // ===================
    // EXAMINATIONS
    // ===================
    async loadExaminations() {
        const upcomingContainer = document.getElementById('upcoming-exams');
        const resultsContainer = document.getElementById('exam-results');

        // Mock data for now
        upcomingContainer.innerHTML = `
            <div class="list-item">
                <h4>Mid-Semester Examination</h4>
                <p>Data Structures (CS201) - Theory</p>
                <span class="date">March 15, 2026 | 10:00 AM</span>
            </div>
            <div class="list-item">
                <h4>Practical Examination</h4>
                <p>Database Management (CS301) - Lab</p>
                <span class="date">March 20, 2026 | 02:00 PM</span>
            </div>
        `;

        resultsContainer.innerHTML = '<p class="empty-state">No results published yet</p>';
    },

    // ===================
    // TIMETABLE
    // ===================
    async loadTimetable() {
        const container = document.getElementById('weekly-timetable');
        const adminActions = document.getElementById('timetable-admin-actions');

        // Show admin buttons for admin/faculty
        if (this.user && ['admin', 'faculty'].includes(this.user.role)) {
            if (adminActions) adminActions.style.display = 'flex';
        } else {
            if (adminActions) adminActions.style.display = 'none';
        }

        // Check if we can manage (admin or faculty)
        const canManage = this.user && ['admin', 'faculty'].includes(this.user.role);
        const isAdmin = this.user && this.user.role === 'admin';

        try {
            const { timetable } = await API.calendar.getTimetable();
            const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

            // Group slots by time
            const timeSlots = {};
            timetable.forEach(slot => {
                const timeKey = `${slot.start_time} - ${slot.end_time}`;
                if (!timeSlots[timeKey]) {
                    timeSlots[timeKey] = {};
                }
                timeSlots[timeKey][slot.day_of_week] = slot;
            });

            // Sort time slots
            const sortedTimes = Object.keys(timeSlots).sort();

            container.innerHTML = `
                <table class="data-table timetable-table">
                    <thead>
                        <tr>
                            <th>Time / Day</th>
                            ${days.slice(0, 5).map((day, i) => `
                                <th>
                                    ${day}
                                    ${canManage ? `<button class="btn-quick-add" onclick="AdminManager.showTimetableForm({day_of_week: ${i}})" title="Add slot">+</button>` : ''}
                                </th>
                            `).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${sortedTimes.length > 0 ? sortedTimes.map(time => `
                            <tr>
                                <td class="time-cell">${time}</td>
                                ${[0, 1, 2, 3, 4].map(dayIndex => {
                const slot = timeSlots[time][dayIndex];
                if (slot) {
                    return `
                                            <td class="slot-cell ${slot.slot_type || ''}">
                                                <div class="slot-content">
                                                    <span class="slot-name">${slot.course_name || slot.course_code || 'Class'}</span>
                                                    ${slot.room ? `<span class="slot-room">${slot.room}</span>` : ''}
                                                    ${canManage ? `
                                                        <div class="slot-actions">
                                                            <button class="btn-slot-edit" onclick="AdminManager.editTimetableSlot('${slot.id}')" title="Edit">✏️</button>
                                                            ${isAdmin ? `<button class="btn-slot-delete" onclick="AdminManager.deleteTimetableSlot('${slot.id}')" title="Delete">🗑️</button>` : ''}
                                                        </div>
                                                    ` : ''}
                                                </div>
                                            </td>
                                        `;
                } else {
                    return `<td class="empty-slot">${canManage ? `<button class="btn-add-empty" onclick="AdminManager.showTimetableForm({day_of_week: ${dayIndex}})" title="Add class">+</button>` : '-'}</td>`;
                }
            }).join('')}
                            </tr>
                        `).join('') : `
                            <tr>
                                <td colspan="6" class="empty-state">
                                    ${canManage ? 'No classes scheduled yet. Click "Add Class Slot" to create your first class.' : 'Timetable not available'}
                                </td>
                            </tr>
                        `}
                    </tbody>
                </table>
            `;
        } catch (error) {
            console.error('Timetable load error:', error);
            // Fallback to mock data
            container.innerHTML = `
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Time / Day</th>
                            <th>Monday</th>
                            <th>Tuesday</th>
                            <th>Wednesday</th>
                            <th>Thursday</th>
                            <th>Friday</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>09:00 - 10:30</td>
                            <td>Data Structures</td>
                            <td>DBMS</td>
                            <td>Data Structures</td>
                            <td>DBMS</td>
                            <td>Algorithms</td>
                        </tr>
                        <tr>
                            <td>11:00 - 12:30</td>
                            <td>DBMS Lab</td>
                            <td>Algorithms</td>
                            <td>Web Dev</td>
                            <td>Algorithms</td>
                            <td>Web Dev</td>
                        </tr>
                        <tr>
                            <td>02:00 - 03:30</td>
                            <td>Web Dev</td>
                            <td>-</td>
                            <td>DS Lab</td>
                            <td>Project</td>
                            <td>Project</td>
                        </tr>
                    </tbody>
                </table>
            `;
        }
    },

    // ===================
    // FEES
    // ===================
    async loadFees() {
        const container = document.getElementById('fee-history');
        // Mock data
        container.innerHTML = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Description</th>
                        <th>Amount</th>
                        <th>Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Tuition Fee - Sem 6</td>
                        <td>₹45,000</td>
                        <td>Jan 15, 2026</td>
                        <td><span class="badge" style="background:var(--success)">Paid</span></td>
                    </tr>
                    <tr>
                        <td>Examination Fee</td>
                        <td>₹2,500</td>
                        <td>Feb 01, 2026</td>
                        <td><span class="badge" style="background:var(--warning)">Pending</span></td>
                    </tr>
                </tbody>
            </table>
        `;
    },

    // ===================
    // BOOKINGS
    // ===================
    async loadBookings() {
        try {
            const data = await API.bookings.getMyBookings();
            const container = document.getElementById('my-bookings');

            if (data.bookings?.length > 0) {
                container.innerHTML = data.bookings.map(b => `
                    <div class="list-item">
                        <h4>${b.room_name || 'Room'}</h4>
                        <p>${b.date} | ${b.start_time} - ${b.end_time}</p>
                        <span class="badge">${b.status}</span>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No bookings</p>';
            }

            const roomsData = await API.bookings.getRooms();
            const roomsContainer = document.getElementById('available-rooms');

            if (roomsData.rooms?.length > 0) {
                roomsContainer.innerHTML = roomsData.rooms.map(r => `
                    <div class="room-card">
                        <h3>${r.name}</h3>
                        <p>Building: ${r.building} | Floor: ${r.floor}</p>
                        <p>Capacity: ${r.capacity} | Type: ${r.room_type}</p>
                    </div>
                `).join('');
            } else {
                roomsContainer.innerHTML = '<p class="empty-state">No rooms available</p>';
            }
        } catch (error) {
            console.error('Bookings error:', error);
        }
    },

    // ===================
    // LIBRARY
    // ===================
    async loadLibrary() {
        const container = document.getElementById('borrowed-books');
        // Mock data
        container.innerHTML = '<p class="empty-state">No books currently borrowed</p>';
    },

    // ===================
    // EVENTS
    // ===================
    async loadEvents() {
        const container = document.getElementById('upcoming-events');
        // Mock data
        container.innerHTML = `
            <div class="list-item">
                <h4>Tech Fest 2026</h4>
                <p>Annual technology festival with hackathons, workshops, and competitions</p>
                <span class="date">April 5-7, 2026</span>
            </div>
            <div class="list-item">
                <h4>Career Fair</h4>
                <p>Connect with top companies and explore job opportunities</p>
                <span class="date">March 25, 2026</span>
            </div>
        `;
    },

    // ===================
    // ANNOUNCEMENTS
    // ===================
    async loadAnnouncements() {
        const container = document.getElementById('announcements-list');
        try {
            const data = await API.announcements.getAll();
            if (data.announcements?.length > 0) {
                container.innerHTML = data.announcements.map(a => `
                    <div class="announcement-card ${a.is_pinned ? 'pinned' : ''}">
                        <h3>
                            ${a.is_pinned ? '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M12 17v5"/><path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z"/></svg> ' : ''}
                            ${a.title}
                        </h3>
                        <div class="announcement-content">${a.content}</div>
                        <div class="announcement-meta">
                            <span>By ${a.author_name}</span>
                            <span>${this.formatShortDate(a.published_at)}</span>
                        </div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No announcements</p>';
            }
        } catch (error) {
            container.innerHTML = '<p class="empty-state">Failed to load announcements</p>';
        }
    },

    // ===================
    // QUIZ
    // ===================
    async loadQuizzes() {
        const availableContainer = document.getElementById('available-quizzes');
        const completedContainer = document.getElementById('completed-quizzes');

        availableContainer.innerHTML = '<p class="empty-state">No quizzes available</p>';
        completedContainer.innerHTML = '<p class="empty-state">No completed quizzes</p>';
    },

    // ===================
    // GRIEVANCE
    // ===================
    async loadGrievances() {
        const container = document.getElementById('my-grievances');
        container.innerHTML = '<p class="empty-state">No grievances submitted</p>';
    },

    showGrievanceForm() {
        const modalBody = `
            <h2>Submit Grievance</h2>
            <div class="form-group">
                <label>Category</label>
                <select id="grievance-category">
                    <option value="academic">Academic</option>
                    <option value="facilities">Facilities</option>
                    <option value="hostel">Hostel</option>
                    <option value="fees">Fees</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="form-group">
                <label>Subject</label>
                <input type="text" id="grievance-subject" placeholder="Brief subject">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="grievance-description" rows="5" placeholder="Describe your grievance in detail..."></textarea>
            </div>
            <button class="btn btn-primary" onclick="App.submitGrievance()">Submit</button>
        `;
        this.showModal(modalBody);
    },

    async submitGrievance() {
        this.showToast('Grievance submitted successfully!', 'success');
        this.closeModal();
    },

    // ===================
    // TPO / PLACEMENT
    // ===================
    async loadTPO() {
        const container = document.getElementById('placement-drives');
        // Mock data
        container.innerHTML = `
            <div class="list-item">
                <h4>Google India</h4>
                <p>Software Engineer | CTC: ₹25-40 LPA</p>
                <span class="date">Applications close: Feb 28, 2026</span>
            </div>
            <div class="list-item">
                <h4>Microsoft</h4>
                <p>Software Development Engineer | CTC: ₹20-35 LPA</p>
                <span class="date">Applications close: Mar 5, 2026</span>
            </div>
        `;
    },

    // ===================
    // FEEDBACK
    // ===================
    async submitFeedback() {
        const category = document.getElementById('feedback-category').value;
        const subject = document.getElementById('feedback-subject').value;
        const message = document.getElementById('feedback-message').value;

        if (!subject || !message) {
            this.showToast('Please fill all fields', 'error');
            return;
        }

        this.showToast('Feedback submitted successfully!', 'success');
        document.getElementById('feedback-form').reset();
    },

    // ===================
    // PROFILE
    // ===================
    loadProfile() {
        document.getElementById('profile-name').value = this.user?.name || '';
        document.getElementById('profile-email').value = this.user?.email || '';
        document.getElementById('profile-dept').value = this.user?.department || '';
        document.getElementById('profile-phone').value = this.user?.phone || '';
    },

    async updateProfile() {
        try {
            const data = {
                name: document.getElementById('profile-name').value,
                department: document.getElementById('profile-dept').value,
                phone: document.getElementById('profile-phone').value
            };

            await API.users.update(this.user.id, data);
            this.user = { ...this.user, ...data };
            localStorage.setItem('campus_user', JSON.stringify(this.user));
            document.getElementById('user-name').textContent = this.user.name;
            this.showToast('Profile updated!', 'success');
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // ===================
    // FORMS
    // ===================
    showCourseForm() {
        const modalBody = `
            <h2>Add New Course</h2>
            <div class="form-group">
                <label>Course Code</label>
                <input type="text" id="course-code" placeholder="CS201">
            </div>
            <div class="form-group">
                <label>Course Name</label>
                <input type="text" id="course-name" placeholder="Data Structures">
            </div>
            <div class="form-group">
                <label>Credits</label>
                <input type="number" id="course-credits" min="1" max="6" value="3">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="course-description" rows="3"></textarea>
            </div>
            <button class="btn btn-primary" onclick="App.createCourse()">Create Course</button>
        `;
        this.showModal(modalBody);
    },

    async createCourse() {
        this.showToast('Course created!', 'success');
        this.closeModal();
        this.loadCourses();
    },

    showAssignmentForm() {
        const modalBody = `
            <h2>Create Assignment</h2>
            <div class="form-group">
                <label>Title</label>
                <input type="text" id="assignment-title" placeholder="Assignment title">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="assignment-desc" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label>Due Date</label>
                <input type="datetime-local" id="assignment-due">
            </div>
            <div class="form-group">
                <label>Max Marks</label>
                <input type="number" id="assignment-marks" value="100">
            </div>
            <button class="btn btn-primary" onclick="App.createAssignment()">Create Assignment</button>
        `;
        this.showModal(modalBody);
    },

    async createAssignment() {
        this.showToast('Assignment created!', 'success');
        this.closeModal();
        this.loadAssignments();
    },

    // Show QR generator (faculty)
    async showQRGenerator() {
        try {
            const coursesData = await API.courses.getAll();
            if (!coursesData.courses?.length) {
                this.showToast('No courses assigned', 'error');
                return;
            }

            const modalBody = `
                <h2>Generate Attendance QR</h2>
                <div class="form-group">
                    <label>Select Course</label>
                    <select id="qr-course">
                        ${coursesData.courses.map(c => `<option value="${c.id}">${c.code} - ${c.name}</option>`).join('')}
                    </select>
                </div>
                <button class="btn btn-primary" onclick="App.generateQR()">Generate QR Code</button>
                <div id="qr-result" style="margin-top: 20px; text-align: center;"></div>
            `;
            this.showModal(modalBody);
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Generate QR
    async generateQR() {
        const courseId = document.getElementById('qr-course').value;
        try {
            const data = await API.attendance.generateQR(courseId);
            document.getElementById('qr-result').innerHTML = `
                <img src="${data.qr_image}" alt="QR Code" style="max-width: 250px; border-radius: 8px;">
                <p style="margin-top: 12px; color: var(--text-muted);">Expires in ${Math.floor(data.expires_in_seconds / 60)} minutes</p>
            `;
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Show QR scanner (student)
    showQRScanner() {
        const modalBody = `
            <h2>Mark Attendance</h2>
            <p style="margin-bottom: 16px; color: var(--text-secondary);">Enter the QR code data shown by your instructor:</p>
            <div class="form-group">
                <label>QR Code Data</label>
                <input type="text" id="qr-input" placeholder="Paste or type QR code data">
            </div>
            <button class="btn btn-primary" onclick="App.markAttendance()">Mark Present</button>
        `;
        this.showModal(modalBody);
    },

    // Mark attendance
    async markAttendance() {
        const qrData = document.getElementById('qr-input').value;
        try {
            const data = await API.attendance.mark(qrData);
            this.showToast(data.message, 'success');
            this.closeModal();
            this.loadAttendance();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Show booking form
    showBookingForm() {
        const modalBody = `
            <h2>Book a Room</h2>
            <div class="form-group">
                <label>Date</label>
                <input type="date" id="booking-date">
            </div>
            <div class="form-group">
                <label>Start Time</label>
                <input type="time" id="booking-start">
            </div>
            <div class="form-group">
                <label>End Time</label>
                <input type="time" id="booking-end">
            </div>
            <div class="form-group">
                <label>Purpose</label>
                <textarea id="booking-purpose" rows="2" placeholder="Meeting purpose..."></textarea>
            </div>
            <button class="btn btn-secondary" onclick="App.checkAvailability()">Check Availability</button>
            <div id="booking-rooms" style="margin-top: 16px;"></div>
        `;
        this.showModal(modalBody);
    },

    // Check availability
    async checkAvailability() {
        const date = document.getElementById('booking-date').value;
        const start = document.getElementById('booking-start').value;
        const end = document.getElementById('booking-end').value;

        try {
            const data = await API.bookings.getAvailable(date, start, end);
            const container = document.getElementById('booking-rooms');

            if (data.rooms?.length > 0) {
                container.innerHTML = '<h4 style="margin-bottom: 12px;">Available Rooms:</h4>' + data.rooms.map(r => `
                    <button class="btn btn-secondary" style="margin: 4px" onclick="App.bookRoom('${r.id}')">${r.name}</button>
                `).join('');
            } else {
                container.innerHTML = '<p class="empty-state">No rooms available for this time slot</p>';
            }
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Book room
    async bookRoom(roomId) {
        const booking = {
            room_id: roomId,
            date: document.getElementById('booking-date').value,
            start_time: document.getElementById('booking-start').value,
            end_time: document.getElementById('booking-end').value,
            purpose: document.getElementById('booking-purpose').value
        };

        try {
            await API.bookings.create(booking);
            this.showToast('Room booked successfully!', 'success');
            this.closeModal();
            this.loadBookings();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // Show announcement form
    showAnnouncementForm() {
        const modalBody = `
            <h2>New Announcement</h2>
            <div class="form-group">
                <label>Title</label>
                <input type="text" id="ann-title" placeholder="Announcement title">
            </div>
            <div class="form-group">
                <label>Content</label>
                <textarea id="ann-content" rows="4" placeholder="Announcement content..."></textarea>
            </div>
            <div class="form-group">
                <label>Category</label>
                <select id="ann-category">
                    <option value="general">General</option>
                    <option value="academic">Academic</option>
                    <option value="event">Event</option>
                    <option value="urgent">Urgent</option>
                </select>
            </div>
            <button class="btn btn-primary" onclick="App.createAnnouncement()">Publish</button>
        `;
        this.showModal(modalBody);
    },

    // Create announcement
    async createAnnouncement() {
        try {
            await API.announcements.create({
                title: document.getElementById('ann-title').value,
                content: document.getElementById('ann-content').value,
                category: document.getElementById('ann-category').value
            });
            this.showToast('Announcement published!', 'success');
            this.closeModal();
            this.loadAnnouncements();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    },

    // ===================
    // MODAL & TOAST
    // ===================
    showModal(content) {
        document.getElementById('modal-body').innerHTML = content;
        document.getElementById('modal').classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    },

    closeModal() {
        document.getElementById('modal').classList.add('hidden');
        document.body.style.overflow = '';
    },

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.classList.remove('hidden');

        setTimeout(() => {
            toast.classList.add('hidden');
        }, 3000);
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => App.init());
