clear;
clc;
close all;

%% Parametres du systeme
m = 100;          % Masse (kg)
c = 1500;         % Coefficient d'amortissement (N.s/m)
x0 = 0;           % Position initiale (m)
v0 = 1;           % Vitesse initiale (m/s)
tfin = 2;            % Duree de simulation (s)

k_list = [10000, 20000, 30000]; % Valeurs de la raideur a comparer

y0 = [x0; v0]; % Conditions initiales

temps = linspace(0, tfin, 2000); % Temps de simulation 

resultats = cell(length(k_list), 1); % Stockage des resultats

%% Simulation
for i = 1:length(k_list)

    k = k_list(i);
    % Resolution de l'equation differentielle
    [t, y] = ode45(@(t,y) equations(t,y,m,c,k), ...
                   temps, y0);

    x = y(:,1);
    v = y(:,2);

    % Calcul de l'acceleration
    a = (-c*v - k*x)/m;

    % Stockage
    resultats{i} = struct('t', t, 'x', x, ...
                          'v', v, 'a', a);

end

%% Graphique 1 : Deplacement
figure;

for i = 1:length(k_list)
    r = resultats{i};

    plot(r.t, r.x, 'LineWidth', 1.5);
    hold on;
end

xlabel('Temps (s)');
ylabel('Deplacement x (m)');
title('Influence de la raideur sur le deplacement');
legend('k = 10000 N/m', 'k = 20000 N/m', ...
       'k = 30000 N/m', 'Location', 'best');
grid on;
hold off;

saveas(gcf, 'influence_raideur_deplacement.png');

%% Graphique 2 : Vitesse
figure;

for i = 1:length(k_list)
    r = resultats{i};

    plot(r.t, r.v, 'LineWidth', 1.5);
    hold on;
end

xlabel('Temps (s)');
ylabel('Vitesse v (m/s)');
title('Influence de la raideur sur la vitesse');
legend('k = 10000 N/m', 'k = 20000 N/m', ...
       'k = 30000 N/m', 'Location', 'best');
grid on;
hold off;

saveas(gcf, 'influence_raideur_vitesse.png');

%% Graphique 3 : Acceleration
figure;

for i = 1:length(k_list)
    r = resultats{i};

    plot(r.t, r.a, 'LineWidth', 1.5);
    hold on;
end

xlabel('Temps (s)');
ylabel('Acceleration a (m/s^2)');
title('Influence de la raideur sur l''acceleration');
legend('k = 10000 N/m', 'k = 20000 N/m', ...
       'k = 30000 N/m', 'Location', 'best');
grid on;
hold off;

saveas(gcf, 'influence_raideur_acceleration.png');

%% Tableau des resultats
k_col = k_list(:);
x_max = zeros(length(k_list), 1);
v_max = zeros(length(k_list), 1);
a_max = zeros(length(k_list), 1);

for i = 1:length(k_list)
    r = resultats{i};

    x_max(i) = max(abs(r.x));
    v_max(i) = max(abs(r.v));
    a_max(i) = max(abs(r.a));
end

Tableau = table(k_col, x_max, v_max, a_max, ...
    'VariableNames', {'k_N_m', 'x_max_m', ...
                      'v_max_m_s', 'a_max_m_s2'});

disp(Tableau);

%% Fonction representant le systeme
function dydt = equations(~, y, m, c, k)

    x = y(1);
    v = y(2);

    a = (-c*v - k*x)/m;

    dydt = [v; a];

end