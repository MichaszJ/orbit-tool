import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from orbital_dynamics import two_body_propagator, three_body_cr_propagator, three_body_propagator
from orbital_elements import ground_track

st.title('Orbit Tool')
st.write('Created by Michal Jagodzinski')

modules = ['Orbit Propagator', 'Ground Track']
module_option = st.selectbox('Choose Module:', modules)

if module_option == 'Orbit Propagator':
    props = ['General Two-Body', 'Circular Restricted Three-Body', 'General Three-Body']
    prop_option = st.selectbox('Choose Propagator:', props)

    st.sidebar.markdown(f'# {prop_option} - Defining Variables')

    if prop_option == 'General Two-Body':
        prop_setup = {
            't_init': 0,
            't_final': 480,
            'mass_1': 1e26,
            'mass_2': 1e26,
            'grav_constant': 6.67259e-11,
            'tolerance': 500,
            'beta': 0.8
        }

        prop_ic = {
            'x_1': 0,
            'y_1': 0,
            'z_1': 0,
            'vx_1': 10e3,
            'vy_1': 20e3,
            'vz_1': 30e3,
            'x_2': 3000e3,
            'y_2': 0,
            'z_2': 0,
            'vx_2': 0,
            'vy_2': 40e3,
            'vz_2': 0
        }

    elif prop_option == 'Circular Restricted Three-Body':
        prop_setup = {
            't_init': 0,
            't_final': 3.16689 * 24 * 60 * 60,
            'mass_1': 5.974e24,
            'mass_2': 73.48e21,
            'r_12': 384400,
            'grav_constant': 6.6759e-20,
            'tolerance': 10,
            'beta': 0.8
        }

        prop_ic = {
            'x': -4671,
            'y': -6378 - 200,
            'z': 0,
            'v_x': 10.2565702,
            'v_y': -3.73308146,
            'v_z': 0
        }

    elif prop_option == 'General Three-Body':
        prop_setup = {
            't_init': 0,
            't_final': 7,
            'mass_1': 1,
            'mass_2': 1,
            'mass_3': 1,
            'grav_constant': 1,
            'tolerance': 0.005,
            'beta': 0.7
        }

        prop_ic = {
            'x_1': -1,
            'y_1': 0,
            'z_1': 0,
            'vx_1': 0.39295,
            'vy_1': 0.09758,
            'vz_1': 0,
            'x_2': 1,
            'y_2': 0,
            'z_2': 0,
            'vx_2': 0.39295,
            'vy_2': 0.09758,
            'vz_2': 0,
            'x_3': 0,
            'y_3': 0,
            'z_3': 0,
            'vx_3': -0.7859,
            'vy_3': -0.19516,
            'vz_3': 0
        }


    st.sidebar.markdown('## Setup')
    for key in prop_setup:
        prop_setup[key] = st.sidebar.text_input(key, float(prop_setup[key]))

    st.sidebar.markdown('## Initial Conditions')
    for key in prop_ic:
        prop_setup[key] = st.sidebar.text_input(key, float(prop_ic[key]))

    pressed = st.sidebar.checkbox('Calculate')

    if pressed:
        for key in prop_setup:
            prop_setup[key] = float(prop_setup[key])

        for key in prop_ic:
            prop_ic[key] = float(prop_ic[key])

        if prop_option == 'General Two-Body':
            s_out, t_out = two_body_propagator(t_init=prop_setup['t_init'],
                                            t_final=prop_setup['t_final'],
                                            mass_1=prop_setup['mass_1'],
                                            mass_2=prop_setup['mass_2'],
                                            initial_conditions=[prop_ic[key] for key in prop_ic],
                                            grav_constant=prop_setup['grav_constant'],
                                            tolerance=prop_setup['tolerance'],
                                            beta=prop_setup['beta'])

            plot_vars = ['t', 'x_1', 'y_1', 'z_1', 'vx_1', 'vy_1', 'vz_1', 'x_2', 'y_2', 'z_2', 'vx_2', 'vy_2', 'vz_2']
            plot_values = {'t': t_out}

        elif prop_option == 'Circular Restricted Three-Body':
            s_out, t_out = three_body_cr_propagator(t_init=prop_setup['t_init'],
                                                    t_final=prop_setup['t_final'],
                                                    mass_1=prop_setup['mass_1'],
                                                    mass_2=prop_setup['mass_2'],
                                                    r_12=prop_setup['r_12'],
                                                    initial_conditions=[prop_ic[key] for key in prop_ic],
                                                    grav_constant=prop_setup['grav_constant'],
                                                    tolerance=prop_setup['tolerance'],
                                                    beta=prop_setup['beta'])

            plot_vars = ['t', 'x', 'y', 'z', 'v_x', 'v_y', 'v_z']
            plot_values = {'t': t_out}

        elif prop_option == 'General Three-Body':
            s_out, t_out = three_body_propagator(t_init=prop_setup['t_init'],
                                                t_final=prop_setup['t_final'],
                                                mass_1=prop_setup['mass_1'],
                                                mass_2=prop_setup['mass_2'],
                                                mass_3=prop_setup['mass_3'],
                                                initial_conditions=[prop_ic[key] for key in prop_ic],
                                                grav_constant=prop_setup['grav_constant'],
                                                tolerance=prop_setup['tolerance'],
                                                beta=prop_setup['beta'])

            plot_vars = ['t', 'x_1', 'y_1', 'z_1', 'vx_1', 'vy_1', 'vz_1', 'x_2', 'y_2', 'z_2', 'vx_2', 'vy_2', 'vz_2', 'x_3', 'y_3', 'z_3', 'vx_3', 'vy_3', 'vz_3']
            plot_values = {'t': t_out}

        for i in range(len(s_out[0])):
            plot_values[plot_vars[i + 1]] = s_out.T[i]

        st.sidebar.write('Solution achieved')
        st.sidebar.write(f'Number of points: {len(s_out.T[0])}')

    st.markdown(f'# {prop_option} - Plotting')

    if pressed:
        num_lines = int(st.text_input('Number of lines to plot', 1))
        threed_plot = st.checkbox('3D Plot?')

        cols = st.columns(int(num_lines))

        lines_vars = [None] * num_lines

        for i in range(num_lines):
            if threed_plot:
                cols[i].markdown(f'### Line {i + 1}')
                lines_vars[i] = [
                    cols[i].selectbox(f'Choose Line {i + 1} x variable:', plot_vars),
                    cols[i].selectbox(f'Choose Line {i + 1} y variable:', plot_vars),
                    cols[i].selectbox(f'Choose Line {i + 1} z variable:', plot_vars)
                ]
            else:
                cols[i].markdown(f'### Line {i + 1}')
                lines_vars[i] = [
                    cols[i].selectbox(f'Choose Line {i + 1} x variable:', plot_vars),
                    cols[i].selectbox(f'Choose Line {i + 1} y variable:', plot_vars)
                ]

        #layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig = go.Figure()
        fig.update_layout(width=1100,height=900)

        for i, line in enumerate(lines_vars):
            if threed_plot:
                fig.add_trace(go.Scatter3d(x=plot_values[line[0]], y=plot_values[line[1]], z=plot_values[line[2]], mode='lines',name=f'Line {i + 1} - {line[1]} vs. {line[0]}'))
            else:
                fig.add_trace(go.Scatter(x=plot_values[line[0]], y=plot_values[line[1]], mode='lines',name=f'Line {i + 1} - {line[1]} vs. {line[0]}'))

        fig.update_yaxes(scaleanchor="x", scaleratio=1)

        if prop_option == 'Circular Restricted Three-Body':
            planet_draw = st.checkbox('Plot masses?')

            if planet_draw:
                m1_col, m2_col = st.columns(2)

                m1_radius = float(m1_col.text_input('Mass 1 Radius', 6378))
                m1_pos_x = float(m1_col.text_input('Mass 1 x', -4671))
                m1_pos_y = float(m1_col.text_input('Mass 1 y', 0))

                m2_radius = float(m2_col.text_input('Mass 2 Radius', 1737))
                m2_pos_x = float(m2_col.text_input('Mass 2 x', -4671 + 384400))
                m2_pos_y = float(m2_col.text_input('Mass 2 y', 0))

                fig.add_shape(type='circle',
                            xref='x',
                            yref='y',
                            x0=m1_pos_x - m1_radius / 2,
                            y0=m1_pos_y - m1_radius / 2,
                            x1=m1_pos_x + m1_radius / 2,
                            y1=m1_pos_y + m1_radius / 2)

                fig.add_shape(type='circle',
                            xref='x',
                            yref='y',
                            x0=m2_pos_x - m2_radius / 2,
                            y0=m2_pos_y - m2_radius / 2,
                            x1=m2_pos_x + m2_radius / 2,
                            y1=m2_pos_y + m2_radius / 2)

        st.plotly_chart(fig, width=1100, height=900)

elif module_option == 'Ground Track':
    st.sidebar.markdown('## Orbital Elements')
    angle_degrees = st.sidebar.checkbox('Use degrees?')

    if angle_degrees:
        elements = {
                    'Semi-Major Axis': 8350, 
                    'Eccentricity': 0.19760, 
                    'Inclination': 60, 
                    'Right Ascension': 270, 
                    'Argument of Perigee': 45, 
                    'True Anomaly': 230
        }
    else:
        elements = {
                'Semi-Major Axis': 8350, 
                'Eccentricity': 0.19760, 
                'Inclination': np.radians(60), 
                'Right Ascension': np.radians(270), 
                'Argument of Perigee': np.radians(45), 
                'True Anomaly': np.radians(230)
        }

    for key in elements:
        elements[key] = st.sidebar.text_input(key, float(elements[key]))

    st.sidebar.markdown('## Options')
    t_init = st.sidebar.text_input('Initial Time (s)', 0.0)
    t_final = st.sidebar.text_input('Final Time (s)', 3.25 * 7593.481415887944)
    num_steps = st.sidebar.text_input('Step Number', 1000)
        
    run_ground_track = st.sidebar.checkbox('Run Ground Track')
    
    if run_ground_track:
        if angle_degrees:
            for key in elements:
                if key in ['Inclination', 'Right Ascension', 'Argument of Perigee', 'True Anomaly']:
                    elements[key] = np.radians(float(elements[key]))
                else:
                    elements[key] = float(elements[key])
        else:
            for key in elements:
                elements[key] = float(elements[key])

        t_init = float(t_init)
        t_final = float(t_final)
        num_steps = int(num_steps)

        elements_list = [elements[key] for key in elements]
        lon, lat = ground_track(elements_list, t_init=t_init, t_final=t_final, num_steps=num_steps)
        lon, lat = np.degrees(lon), np.degrees(lat)

        fig = go.Figure()
        fig.add_trace(go.Scattergeo(lat=lat, lon=lon))
        st.plotly_chart(fig)