FROM julia

RUN julia -e 'using Pkg; Pkg.add("HTTP")'
RUN julia -e 'using Pkg; Pkg.add("JSON")'
RUN julia -e 'using Pkg; Pkg.add("LibPQ")'
RUN julia -e 'using Pkg; Pkg.add("Tables")'


COPY pizza_bot.jl /home/
COPY psql_backend.jl /home/
WORKDIR /home/

ENTRYPOINT julia pizza_bot.jl
